// ============================================================================
// NEO4J GRAPH VISUALIZATION QUERIES
// Queries optimized for Neo4j Browser and Bloom visualization
// ============================================================================

// 1. FULL ECOSYSTEM OVERVIEW
// ============================================================================

// Complete graph (all nodes and relationships) - Limited to prevent browser overload
MATCH (n)
OPTIONAL MATCH (n)-[r]-(m)
WHERE n.company_id IS NOT NULL OR n.investor_id IS NOT NULL
RETURN n, r, m
LIMIT 100;

// High-level ecosystem structure
MATCH (c:Company)-[r1]->(l:Location)
MATCH (c)-[r2]->(s:Sector)
MATCH (f:Fund)-[r3]->(c)
MATCH (i:Investor)-[r4]->(f)
RETURN c, r1, l, r2, s, r3, f, r4, i
LIMIT 50;

// 2. INVESTOR PORTFOLIO VISUALIZATION
// ============================================================================

// Single investor with full portfolio
MATCH (i:Investor {investor_id: 'I1'})-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
OPTIONAL MATCH (c)-[:LOCATED_IN]->(l:Location)
OPTIONAL MATCH (c)-[:OPERATES_IN]->(s:Sector)
RETURN i, f, c, l, s;

// Investor network (all investors + shared investments)
MATCH (i1:Investor)-[:MANAGES]-(f:Fund)-[:INVESTED_IN]->(c:Company)<-[:INVESTED_IN]-(f2:Fund)-[:MANAGES]-(i2:Investor)
WITH i1, i2, count(distinct c) as shared_count
WHERE shared_count > 0
RETURN i1, i2, shared_count
LIMIT 20;

// Fund structure with companies and sectors
MATCH (i:Investor)-[:MANAGES]->(f:Fund)
OPTIONAL MATCH (f)-[:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
OPTIONAL MATCH (c)-[:LOCATED_IN]->(l:Location)
RETURN i, f, c, s, l;

// 3. COMPANY ECOSYSTEM
// ============================================================================

// Single company with all relationships
MATCH (c:Company {company_id: 'C1'})
OPTIONAL MATCH (c)-[:LOCATED_IN]->(l:Location)
OPTIONAL MATCH (c)-[:OPERATES_IN]->(s:Sector)
OPTIONAL MATCH (f:Fund)-[:INVESTED_IN]->(c)
OPTIONAL MATCH (f)-[:MANAGES]-(i:Investor)
OPTIONAL MATCH (p:Person)-[:WORKS_AT]->(c)
OPTIONAL MATCH (p)-[:BOARD_MEMBER_OF]->(c)
RETURN c, l, s, f, i, p;

// Company networks (similar stage/sector)
MATCH (c1:Company)-[:OPERATES_IN]->(s:Sector)<-[:OPERATES_IN]-(c2:Company)
MATCH (c1)-[:LOCATED_IN]->(l:Location)
MATCH (c2)-[:LOCATED_IN]->(l)
WHERE c1.company_id < c2.company_id
AND c1.stage = c2.stage
RETURN c1, s, c2, l
LIMIT 30;

// Companies by geographic region
MATCH (l:Location)<-[:LOCATED_IN]-(c:Company)
OPTIONAL MATCH (c)-[:OPERATES_IN]->(s:Sector)
OPTIONAL MATCH (f:Fund)-[:INVESTED_IN]->(c)
RETURN l, c, s, f
ORDER BY l.location_name
LIMIT 50;

// 4. PEOPLE & NETWORK VISUALIZATION
// ============================================================================

// Person network (strong connections)
MATCH (p1:Person)-[k:KNOWS]->(p2:Person)
WHERE k.strength = 'strong'
OPTIONAL MATCH (p1)-[:WORKS_AT]->(c1:Company)
OPTIONAL MATCH (p1)-[:WORKS_FOR]->(i1:Investor)
OPTIONAL MATCH (p2)-[:WORKS_AT]->(c2:Company)
OPTIONAL MATCH (p2)-[:WORKS_FOR]->(i2:Investor)
RETURN p1, k, p2, c1, i1, c2, i2
LIMIT 30;

// Full person ecosystem
MATCH (p:Person)
OPTIONAL MATCH (p)-[:WORKS_AT]->(c:Company)
OPTIONAL MATCH (p)-[:WORKS_FOR]->(i:Investor)
OPTIONAL MATCH (p)-[:BOARD_MEMBER_OF]->(c2:Company)
OPTIONAL MATCH (p)-[k:KNOWS]-(other:Person)
RETURN p, c, i, c2, k, other
LIMIT 50;

// Leadership visualization (founders + executives)
MATCH (p:Person)
WHERE p.role IN ['Founder', 'CEO', 'CTO', 'Managing Partner', 'Partner']
OPTIONAL MATCH (p)-[:WORKS_AT]->(c:Company)
OPTIONAL MATCH (p)-[:WORKS_FOR]->(i:Investor)
OPTIONAL MATCH (p)-[k:KNOWS]-(other:Person)
RETURN p, c, i, k, other
LIMIT 40;

// 5. DEAL FLOW VISUALIZATION
// ============================================================================

// Investment cascade (fund to company to sector)
MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
MATCH (c)-[:LOCATED_IN]->(l:Location)
OPTIONAL MATCH (f)-[:MANAGES]-(i:Investor)
RETURN i, f, inv, c, l, s
ORDER BY inv.year, inv.amount_usd DESC
LIMIT 30;

// Multi-round investments (companies attracting repeat capital)
MATCH (c:Company)<-[inv1:INVESTED_IN]-(f1:Fund)
MATCH (c)<-[inv2:INVESTED_IN]-(f2:Fund)
WHERE inv1.year < inv2.year
OPTIONAL MATCH (f1)-[:MANAGES]-(i1:Investor)
OPTIONAL MATCH (f2)-[:MANAGES]-(i2:Investor)
OPTIONAL MATCH (c)-[:OPERATES_IN]->(s:Sector)
RETURN f1, inv1, f2, inv2, c, s, i1, i2
ORDER BY inv2.year DESC
LIMIT 25;

// Geographic investment flows
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[inv:INVESTED_IN]->(c:Company)-[:LOCATED_IN]->(l:Location)
RETURN i, f, inv, c, l
LIMIT 40;

// 6. SECTOR DEEP DIVES
// ============================================================================

// Sector ecosystem (all companies in sector + investors)
MATCH (s:Sector)<-[:OPERATES_IN]-(c:Company)
OPTIONAL MATCH (c)-[:LOCATED_IN]->(l:Location)
OPTIONAL MATCH (f:Fund)-[:INVESTED_IN]->(c)
OPTIONAL MATCH (f)-[:MANAGES]-(i:Investor)
WHERE s.sector_name = 'AI'
RETURN s, c, l, f, i;

// Sector competition (multiple investors same sector)
MATCH (s:Sector)<-[:OPERATES_IN]-(c:Company)<-[:INVESTED_IN]-(f:Fund)-[:MANAGES]-(i:Investor)
RETURN s, c, f, i
LIMIT 50;

// 7. INFLUENCE & POWER NETWORKS
// ============================================================================

// Power players (multi-portfolio investors)
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
OPTIONAL MATCH (c)-[:OPERATES_IN]->(s:Sector)
RETURN i, f, c, s
ORDER BY i.name
LIMIT 50;

// LP network visualization
MATCH (lp:Investor)-[commit:COMMITS_TO]->(f:Fund)
OPTIONAL MATCH (f)-[:MANAGES]-(gp:Investor)
OPTIONAL MATCH (f)-[:INVESTED_IN]->(c:Company)
RETURN lp, commit, f, gp, c
LIMIT 40;

// 8. EXPLORATION STARTING POINTS
// ============================================================================

// All companies (limited set)
MATCH (c:Company)
OPTIONAL MATCH (c)-[:LOCATED_IN]->(l:Location)
OPTIONAL MATCH (c)-[:OPERATES_IN]->(s:Sector)
RETURN c, l, s
ORDER BY c.company_id
LIMIT 50;

// All investors (limited set)
MATCH (i:Investor)
OPTIONAL MATCH (i)-[:MANAGES|COMMITS_TO]->(f:Fund)
RETURN i, f
ORDER BY i.investor_id
LIMIT 50;

// All funds with structure
MATCH (f:Fund)
OPTIONAL MATCH (i:Investor)-[:MANAGES]->(f)
OPTIONAL MATCH (lp:Investor)-[:COMMITS_TO]->(f)
OPTIONAL MATCH (f)-[:INVESTED_IN]->(c:Company)
RETURN f, i, lp, c
ORDER BY f.fund_id
LIMIT 50;

// All sectors with companies
MATCH (s:Sector)<-[:OPERATES_IN]-(c:Company)
RETURN s, c
ORDER BY s.sector_name
LIMIT 50;

// All locations with companies
MATCH (l:Location)<-[:LOCATED_IN]-(c:Company)
RETURN l, c
ORDER BY l.location_name
LIMIT 50;

// 9. CUSTOM BLOOM VISUALIZATIONS
// ============================================================================

// Recommended perspective: Rich network view
// Use: MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
//      RETURN i, f, c

// Recommended filter path: Investor -> Fund -> Company -> Sector
// Shows investment decision flow

// Recommended graph cards:
// - Investor: name, investor_type, hq_country
// - Fund: name, vintage, strategy
// - Company: name, stage, sector
// - Sector: sector_name
// - Location: location_name
// - Person: name, role
