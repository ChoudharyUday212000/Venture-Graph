// ============================================================================
// NEO4J GRAPH TRAVERSAL & PATH QUERIES
// Advanced traversal patterns for insights
// ============================================================================

// 1. SHORTEST PATH ANALYSIS
// ============================================================================

// Shortest path between two companies
MATCH (c1:Company {company_id: 'C1'}),
      (c2:Company {company_id: 'C10'})
MATCH path = shortestPath((c1)-[*]-(c2))
RETURN path;

// Shortest path between investor and company
MATCH (i:Investor {investor_id: 'I1'}),
      (c:Company {company_id: 'C5'})
MATCH path = shortestPath((i)-[*]-(c))
RETURN path;

// All paths between two companies (limited depth)
MATCH (c1:Company {company_id: 'C1'}),
      (c2:Company {company_id: 'C8'})
MATCH path = (c1)-[*1..3]-(c2)
RETURN path
LIMIT 5;

// 2. TRAVERSAL DEPTH ANALYSIS
// ============================================================================

// N-hops from company (companies within 3 degrees)
MATCH (start:Company {company_id: 'C1'})-[*1..3]-(target:Company)
RETURN distinct target.name as connected_company,
       target.stage as stage,
       target.sector as sector;

// Fund to fund connections (via shared LP)
MATCH (f1:Fund {fund_id: 'F1'})-[:MANAGES]-(i:Investor)-[:MANAGES]-(f2:Fund)
WHERE f1.fund_id <> f2.fund_id
RETURN distinct f2.name as connected_fund,
       f2.vintage as vintage,
       f2.strategy as strategy;

// N-levels of investment (tracking capital flow)
MATCH (gp:Investor {investor_id: 'I1'})-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
RETURN gp.name as investor,
       f.name as fund,
       c.name as company,
       c.stage as company_stage;

// 3. RECOMMENDATION ENGINES
// ============================================================================

// Companies similar to target (same sector/stage/location)
MATCH (target:Company {company_id: 'C1'})
MATCH (target)-[:OPERATES_IN]->(s:Sector)<-[:OPERATES_IN]-(similar:Company)
MATCH (similar)-[:LOCATED_IN]->(l:Location)
MATCH (target)-[:LOCATED_IN]->(l)
WHERE similar.company_id <> target.company_id
AND similar.stage = target.stage
RETURN similar.name as company,
       similar.stage as stage,
       similar.sector as sector,
       "match_score: 3/3" as similarity;

// Co-investment opportunities (companies not yet co-invested)
MATCH (i:Investor {investor_id: 'I1'})-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c1:Company)
MATCH (i)-[:MANAGES]->(f2:Fund)-[:INVESTED_IN]->(c2:Company)
WHERE c1.company_id <> c2.company_id
AND NOT ((f)-[:INVESTED_IN]->(c2))
RETURN distinct c2.name as potential_coinvestment,
       c2.stage as stage,
       c2.sector as sector;

// Sectors an investor should explore
MATCH (i:Investor {investor_id: 'I1'})-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
WITH i, s, count(distinct c) as company_count
MATCH (all_sectors:Sector)
WHERE NOT (all_sectors) IN [s]
RETURN all_sectors.sector_name as unexplored_sector;

// 4. INFLUENCE & AUTHORITY ANALYSIS
// ============================================================================

// Most central investors (by combined portfolio reach)
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
RETURN i.name as investor,
       count(distinct c) as portfolio_breadth,
       count(distinct f) as fund_count,
       collect(distinct c.name) as companies;

// Influential people bridging domains
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
MATCH (p)-[:WORKS_FOR]->(i:Investor)
MATCH (p)-[k:KNOWS]-(other:Person)
WHERE k.strength IN ['strong', 'medium']
RETURN p.name as person,
       p.role as role,
       c.name as company,
       i.name as investor,
       count(other) as network_size;

// Strong connector network
MATCH (p1:Person)-[k1:KNOWS]->(p2:Person)-[k2:KNOWS]->(p3:Person)
WHERE k1.strength = 'strong' AND k2.strength = 'strong'
RETURN p1.name as person1,
       p2.name as central_person,
       p3.name as person3,
       "strong connection chain" as path_quality;

// 5. FUNDING JOURNEY TRACKING
// ============================================================================

// Track company funding progression
MATCH (c:Company {company_id: 'C2'})
MATCH (f:Fund)-[inv:INVESTED_IN]->(c)
RETURN c.name as company,
       c.sector as sector,
       inv.round as funding_round,
       inv.year as year,
       inv.amount_usd as amount,
       f.name as fund
ORDER BY inv.year;

// Investor's exit opportunities (companies progressing to later stages)
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[inv:INVESTED_IN]->(c:Company)
WHERE c.stage IN ['Series B', 'Series C']
RETURN c.name as growth_company,
       c.stage as current_stage,
       inv.round as initial_investment,
       inv.year as investment_year,
       i.name as investor;

// Capital deployment timeline
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)
WITH f, inv.year as year, sum(inv.amount_usd) as yearly_deployed
RETURN f.name as fund,
       year,
       yearly_deployed,
       f.vintage as fund_vintage
ORDER BY f.name, year;

// 6. NETWORK CLUSTERS & COMMUNITIES
// ============================================================================

// Cohesive investor groups (all connected)
MATCH (i1:Investor)-[:MANAGES]-(f:Fund)-[:INVESTED_IN]->(c:Company)<-[:INVESTED_IN]-(f2:Fund)-[:MANAGES]-(i2:Investor)
MATCH (i2)-[:MANAGES]-(f3:Fund)-[:INVESTED_IN]->(c2:Company)<-[:INVESTED_IN]-(f4:Fund)-[:MANAGES]-(i1)
RETURN collect(distinct i1.name + ", " + i2.name) as investor_cluster,
       count(distinct c) as shared_investments;

// Sector-focused investment clubs
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
WITH s, collect(distinct i.name) as investors, count(distinct c) as companies
RETURN s.sector_name as sector,
       investors,
       companies,
       "investors focused on sector" as cluster_type;

// Geographic hubs
MATCH (l:Location)<-[:LOCATED_IN]-(c:Company)<-[:INVESTED_IN]-(f:Fund)-[:MANAGES]-(i:Investor)
RETURN l.location_name as hub,
       collect(distinct i.name) as active_investors,
       count(distinct c) as companies_in_region,
       count(distinct f) as funds_active;

// 7. OPPORTUNITY DISCOVERY
// ============================================================================

// Unexploited geographic opportunities
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)-[:LOCATED_IN]->(l1:Location)
WITH i, l1, count(distinct c) as investments
MATCH (all_locations:Location)
WHERE all_locations.location_name <> l1.location_name
AND NOT (i)-[:MANAGES]->(any_fund:Fund)-[:INVESTED_IN]->(any_c:Company)-[:LOCATED_IN]->(all_locations)
RETURN i.name as investor,
       all_locations.location_name as unexplored_market;

// Emerging trends (new rounds in unexpected combinations)
MATCH (c:Company)<-[inv:INVESTED_IN]-(f:Fund)
WHERE inv.year >= 2023
MATCH (c)-[:OPERATES_IN]->(s:Sector)
MATCH (c)-[:LOCATED_IN]->(l:Location)
RETURN distinct c.name as emerging_company,
       s.sector_name as sector,
       l.location_name as location,
       c.stage as current_stage,
       inv.year as recent_investment_year
ORDER BY inv.year DESC;

// LP allocation opportunities
MATCH (lp:Investor {investor_type: 'LP'})-[commit:COMMITS_TO]->(f:Fund)
WITH lp, count(distinct f) as fund_count, sum(commit.commitment_usd) as total_committed
MATCH (all_funds:Fund)
WHERE NOT (lp)-[:COMMITS_TO]->(all_funds)
RETURN lp.name as lp_name,
       fund_count as current_funds,
       total_committed as committed_capital,
       all_funds.name as opportunity_fund,
       all_funds.vintage as fund_vintage;

// 8. PERFORMANCE ANALYTICS
// ============================================================================

// Fund performance by investment strategy
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)
RETURN f.name as fund,
       f.strategy as strategy,
       count(inv) as num_investments,
       sum(inv.amount_usd) as capital_deployed,
       avg(inv.amount_usd) as avg_check,
       count(distinct c.stage) as stage_diversity;

// Investor track record (hit rate)
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[inv:INVESTED_IN]->(c:Company)
WHERE c.stage IN ['Series B', 'Series C']
WITH i, count(distinct c) as growth_stage_hits,
     count(distinct f) as total_funds
RETURN i.name as investor,
       growth_stage_hits as successful_bets,
       total_funds as portfolio_size,
       (growth_stage_hits * 100 / total_funds) as success_rate;

// 9. RISK ANALYSIS
// ============================================================================

// Concentration risk (overdependence on single investor)
MATCH (c:Company)<-[:INVESTED_IN]-(f:Fund)-[:MANAGES]-(i:Investor)
WITH c, count(distinct i) as investor_diversity
WHERE investor_diversity < 2
RETURN c.name as company,
       c.stage as stage,
       investor_diversity as investor_count,
       "single investor risk" as risk_type;

// Geographic concentration
MATCH (f:Fund)-[:INVESTED_IN]->(c:Company)-[:LOCATED_IN]->(l:Location)
WITH f, collect(l.location_name) as locations
WHERE size(locations) = 1
RETURN f.name as fund,
       locations[0] as concentrated_in,
       "geographic concentration" as risk;
