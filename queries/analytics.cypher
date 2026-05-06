// ============================================================================
// NEO4J GRAPH ANALYTICS QUERIES
// Advanced graph analytics for venture capital ecosystem
// ============================================================================

// 1. INVESTMENT FLOW ANALYSIS
// ============================================================================

// Total capital deployed by each investor
MATCH (i:Investor)-[:MANAGES|COMMITS_TO]-(f:Fund)-[inv:INVESTED_IN]->(c:Company)
RETURN i.name as investor,
       i.investor_type as type,
       count(distinct f) as funds_involved,
       count(distinct c) as companies_invested,
       sum(inv.amount_usd) as total_deployed_usd,
       avg(inv.amount_usd) as avg_check_size_usd
ORDER BY total_deployed_usd DESC;

// Capital deployment by funding stage
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)
RETURN c.stage as funding_stage,
       count(inv) as investments,
       sum(inv.amount_usd) as total_usd,
       avg(inv.amount_usd) as avg_check_usd,
       count(distinct f) as unique_funds
ORDER BY total_usd DESC;

// Capital deployment by sector
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
RETURN s.sector_name as sector,
       count(distinct c) as companies,
       count(inv) as investments,
       sum(inv.amount_usd) as total_usd
ORDER BY total_usd DESC;

// Geographic capital deployment
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)-[:LOCATED_IN]->(l:Location)
RETURN l.location_name as location,
       count(distinct c) as companies,
       count(inv) as investments,
       sum(inv.amount_usd) as total_usd,
       count(distinct f) as funds
ORDER BY total_usd DESC;

// 2. NETWORK ANALYSIS
// ============================================================================

// Most connected investors (by portfolio)
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
WITH i, count(distinct c) as portfolio_size, collect(distinct c.name) as companies
RETURN i.name as investor,
       portfolio_size,
       companies
ORDER BY portfolio_size DESC;

// Investor-to-Investor network via shared investments
MATCH (i1:Investor)-[:MANAGES]-(f:Fund)-[:INVESTED_IN]->(c:Company)<-[:INVESTED_IN]-(f2:Fund)-[:MANAGES]-(i2:Investor)
WHERE i1.investor_id < i2.investor_id
RETURN i1.name as investor1,
       i2.name as investor2,
       count(distinct c) as shared_investments,
       collect(distinct c.name) as companies
ORDER BY shared_investments DESC;

// Company-to-Company network via same investors
MATCH (c1:Company)<-[:INVESTED_IN]-(f:Fund)-[:INVESTED_IN]->(c2:Company)
WHERE c1.company_id < c2.company_id
RETURN c1.name as company1,
       c2.name as company2,
       count(distinct f) as shared_funds,
       collect(f.name) as funds
ORDER BY shared_funds DESC;

// 3. CENTRALITY & INFLUENCE
// ============================================================================

// Most influential people (by network strength)
MATCH (p:Person)-[k:KNOWS]-(other:Person)
RETURN p.name as person,
       p.role as role,
       count(distinct other) as network_size,
       collect(distinct other.name) as connections,
       sum(case k.strength when 'strong' then 3 when 'medium' then 2 else 1 end) as influence_score
ORDER BY influence_score DESC;

// People bridging companies and investors
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
MATCH (p)-[:WORKS_FOR]->(i:Investor)
RETURN p.name as person,
       p.role as role,
       c.name as company,
       i.name as investor,
       "bridge" as connection_type;

// Most connected funds (by investment reach)
MATCH (f:Fund)-[:INVESTED_IN]->(c:Company)
RETURN f.name as fund,
       f.vintage as vintage,
       f.strategy as strategy,
       count(distinct c) as investments,
       sum(c.stage) as portfolio_stages
ORDER BY investments DESC;

// 4. PORTFOLIO ANALYSIS
// ============================================================================

// Portfolio composition by stage
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[inv:INVESTED_IN]->(c:Company)
WITH i, f, c.stage as stage, count(inv) as stage_count
RETURN i.name as investor,
       f.name as fund,
       stage,
       stage_count
ORDER BY i.name, f.name, stage;

// Investor specialization (dominant sectors)
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
WITH i, s.sector_name as sector, count(distinct c) as sector_investments
RETURN i.name as investor,
       sector,
       sector_investments,
       sector_investments * 100 / sum(sector_investments) OVER (PARTITION BY i) as pct_portfolio
ORDER BY i.name, sector_investments DESC;

// Fund performance metrics
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)
RETURN f.name as fund,
       f.vintage as vintage,
       f.strategy as strategy,
       count(inv) as num_investments,
       sum(inv.amount_usd) as deployed_capital,
       avg(inv.amount_usd) as avg_check_size,
       collect(distinct c.stage) as stages_covered
ORDER BY deployed_capital DESC;

// 5. LP COMMITMENT ANALYSIS
// ============================================================================

// LP portfolio across funds
MATCH (lp:Investor)-[commit:COMMITS_TO]->(f:Fund)
WHERE lp.investor_type = 'LP'
RETURN lp.name as lp_name,
       count(distinct f) as num_funds,
       sum(commit.commitment_usd) as total_committed,
       collect(f.name) as funds
ORDER BY total_committed DESC;

// GP success by LP backing
MATCH (lp:Investor)-[commit:COMMITS_TO]->(f:Fund)<-[:MANAGES]-(gp:Investor)
RETURN gp.name as gp_name,
       count(distinct lp) as lp_count,
       sum(commit.commitment_usd) as total_lp_capital,
       collect(distinct lp.name) as lps
ORDER BY total_lp_capital DESC;

// 6. TEMPORAL ANALYSIS
// ============================================================================

// Investment trend over years
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)
RETURN inv.year as investment_year,
       count(inv) as deals,
       sum(inv.amount_usd) as capital_deployed,
       avg(inv.amount_usd) as avg_deal_size
ORDER BY investment_year;

// Fund vintage distribution
MATCH (f:Fund)
RETURN f.vintage as year,
       count(*) as num_funds,
       collect(f.name) as funds
ORDER BY year DESC;

// 7. GROWTH & SCALING
// ============================================================================

// Series progression (companies that moved through funding stages)
MATCH (f1:Fund)-[inv1:INVESTED_IN]->(c:Company)<-[inv2:INVESTED_IN]-(f2:Fund)
WHERE inv1.round < inv2.round
RETURN c.name as company,
       c.sector as sector,
       c.stage as current_stage,
       inv1.round as first_investment,
       inv2.round as follow_on,
       inv1.amount_usd as first_check,
       inv2.amount_usd as follow_check,
       inv2.amount_usd - inv1.amount_usd as check_increase
ORDER BY check_increase DESC;

// Companies with multiple rounds (repeat investors)
MATCH (c:Company)<-[inv:INVESTED_IN]-(f:Fund)
RETURN c.name as company,
       c.sector as sector,
       count(inv) as investment_rounds,
       count(distinct f) as unique_funds,
       sum(inv.amount_usd) as total_raised,
       max(inv.year) - min(inv.year) as years_active
ORDER BY investment_rounds DESC;

// 8. SECTOR ANALYSIS
// ============================================================================

// Sector market landscape
MATCH (s:Sector)<-[:OPERATES_IN]-(c:Company)
OPTIONAL MATCH (c)<-[inv:INVESTED_IN]-(f:Fund)
RETURN s.sector_name as sector,
       count(distinct c) as companies,
       count(distinct inv) as investment_rounds,
       sum(inv.amount_usd) as total_capital,
       collect(distinct c.stage) as stages
ORDER BY total_capital DESC;

// Sector specialization by investors
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
WITH i, s, count(distinct c) as company_count
ORDER BY i.name, company_count DESC
RETURN i.name as investor,
       collect({sector: s.sector_name, companies: company_count}) as sector_focus
ORDER BY i.name;
