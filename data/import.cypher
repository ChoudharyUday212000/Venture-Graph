// Assumes the CSV files are placed in Neo4j import directory.
// Run constraints.cypher first.

LOAD CSV WITH HEADERS FROM 'file:///companies.csv' AS row
MERGE (c:Company {company_id: row.company_id})
SET c.name = row.name, c.sector = row.sector, c.stage = row.stage, c.country = row.country;

LOAD CSV WITH HEADERS FROM 'file:///investors.csv' AS row
MERGE (i:Investor {investor_id: row.investor_id})
SET i.name = row.name, i.investor_type = row.investor_type, i.hq_country = row.hq_country;

LOAD CSV WITH HEADERS FROM 'file:///funds.csv' AS row
MERGE (f:Fund {fund_id: row.fund_id})
SET f.name = row.name, f.vintage = toInteger(row.vintage), f.strategy = row.strategy;

LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (p:Person {person_id: row.person_id})
SET p.name = row.name, p.role = row.role;

LOAD CSV WITH HEADERS FROM 'file:///sectors.csv' AS row
MERGE (s:Sector {sector_name: row.sector_name});

LOAD CSV WITH HEADERS FROM 'file:///locations.csv' AS row
MERGE (l:Location {location_name: row.location_name});

LOAD CSV WITH HEADERS FROM 'file:///investor_manages_fund.csv' AS row
MATCH (i:Investor {investor_id: row.investor_id})
MATCH (f:Fund {fund_id: row.fund_id})
MERGE (i)-[:MANAGES]->(f);

LOAD CSV WITH HEADERS FROM 'file:///lp_commits_fund.csv' AS row
MATCH (i:Investor {investor_id: row.lp_investor_id})
MATCH (f:Fund {fund_id: row.fund_id})
MERGE (i)-[r:COMMITTED_TO]->(f)
SET r.commitment_usd = toInteger(row.commitment_usd), r.year = toInteger(row.year);

LOAD CSV WITH HEADERS FROM 'file:///fund_invested_in_company.csv' AS row
MATCH (f:Fund {fund_id: row.fund_id})
MATCH (c:Company {company_id: row.company_id})
MERGE (f)-[r:INVESTED_IN]->(c)
SET r.round = row.round, r.year = toInteger(row.year), r.amount_usd = toInteger(row.amount_usd);

LOAD CSV WITH HEADERS FROM 'file:///person_works_at_company.csv' AS row
MATCH (p:Person {person_id: row.person_id})
MATCH (c:Company {company_id: row.company_id})
MERGE (p)-[r:WORKS_AT]->(c)
SET r.title = row.title;

LOAD CSV WITH HEADERS FROM 'file:///person_works_for_investor.csv' AS row
MATCH (p:Person {person_id: row.person_id})
MATCH (i:Investor {investor_id: row.investor_id})
MERGE (p)-[r:WORKS_FOR]->(i)
SET r.title = row.title;

LOAD CSV WITH HEADERS FROM 'file:///person_board_member_company.csv' AS row
MATCH (p:Person {person_id: row.person_id})
MATCH (c:Company {company_id: row.company_id})
MERGE (p)-[r:BOARD_MEMBER_OF]->(c)
SET r.since_year = toInteger(row.since_year);

LOAD CSV WITH HEADERS FROM 'file:///person_knows_person.csv' AS row
MATCH (p1:Person {person_id: row.person1_id})
MATCH (p2:Person {person_id: row.person2_id})
MERGE (p1)-[r:KNOWS]->(p2)
SET r.strength = row.strength;

LOAD CSV WITH HEADERS FROM 'file:///company_operates_in_sector.csv' AS row
MATCH (c:Company {company_id: row.company_id})
MATCH (s:Sector {sector_name: row.sector_name})
MERGE (c)-[:OPERATES_IN]->(s);

LOAD CSV WITH HEADERS FROM 'file:///company_located_in_location.csv' AS row
MATCH (c:Company {company_id: row.company_id})
MATCH (l:Location {location_name: row.location_name})
MERGE (c)-[:LOCATED_IN]->(l);
