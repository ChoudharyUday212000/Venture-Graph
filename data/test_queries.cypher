// 1. Which funds invested in C3?
MATCH (f:Fund)-[r:INVESTED_IN]->(c:Company {company_id:'C3'})
RETURN f.fund_id, f.name, r.round, r.year, r.amount_usd;

// 2. Which GPs are linked to C3 through funds?
MATCH (i:Investor {investor_type:'GP'})-[:MANAGES]->(:Fund)-[:INVESTED_IN]->(c:Company {company_id:'C3'})
RETURN DISTINCT i.investor_id, i.name;

// 3. Which LPs are indirectly exposed to C3 through funds?
MATCH (lp:Investor {investor_type:'LP'})-[:COMMITTED_TO]->(:Fund)-[:INVESTED_IN]->(c:Company {company_id:'C3'})
RETURN DISTINCT lp.investor_id, lp.name;

// 4. Board members connected to C2
MATCH (p:Person)-[r:BOARD_MEMBER_OF]->(c:Company {company_id:'C2'})
RETURN p.person_id, p.name, r.since_year;

// 5. People who know a board member of C2
MATCH (x:Person)-[:KNOWS]->(p:Person)-[:BOARD_MEMBER_OF]->(c:Company {company_id:'C2'})
RETURN DISTINCT x.person_id, x.name, p.name AS board_member;

// 6. Companies co-invested in by the same fund as C8
MATCH (:Company {company_id:'C8'})<-[:INVESTED_IN]-(f:Fund)-[:INVESTED_IN]->(other:Company)
WHERE other.company_id <> 'C8'
RETURN DISTINCT f.fund_id, other.company_id, other.name;

// 7. All paths from LP I8 to company C3 up to 4 hops
MATCH p = (lp:Investor {investor_id:'I8'})-[*..4]-(c:Company {company_id:'C3'})
RETURN p LIMIT 20;

// 8. Companies connected through shared investors
MATCH (c1:Company)<-[:INVESTED_IN]-(:Fund)<-[:MANAGES]-(i:Investor {investor_type:'GP'})-[:MANAGES]->(:Fund)-[:INVESTED_IN]->(c2:Company)
WHERE c1.company_id < c2.company_id
RETURN DISTINCT c1.company_id, c2.company_id, i.investor_id;

// 9. People connected through shared investor affiliation
MATCH (p1:Person)-[:WORKS_FOR]->(i:Investor)<-[:WORKS_FOR]-(p2:Person)
WHERE p1.person_id < p2.person_id
RETURN p1.person_id, p2.person_id, i.investor_id;

// 10. Find all companies in India with LP exposure from UAE LPs
MATCH (lp:Investor {investor_type:'LP', hq_country:'UAE'})-[:COMMITTED_TO]->(:Fund)-[:INVESTED_IN]->(c:Company {country:'India'})
RETURN DISTINCT lp.investor_id, c.company_id, c.name;

// 11. Multi-hop people network from P1 up to 3 hops
MATCH p = (:Person {person_id:'P1'})-[:KNOWS*1..3]-(:Person)
RETURN p LIMIT 20;

// 12. Which companies are connected to GP I1 via any 2-hop or 3-hop path?
MATCH p = (i:Investor {investor_id:'I1'})-[*2..3]-(c:Company)
RETURN DISTINCT c.company_id, c.name, length(p) AS hops
ORDER BY hops, c.company_id;
