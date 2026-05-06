// Uniqueness constraints
CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.company_id IS UNIQUE;
CREATE CONSTRAINT investor_id_unique IF NOT EXISTS FOR (i:Investor) REQUIRE i.investor_id IS UNIQUE;
CREATE CONSTRAINT fund_id_unique IF NOT EXISTS FOR (f:Fund) REQUIRE f.fund_id IS UNIQUE;
CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.person_id IS UNIQUE;
CREATE CONSTRAINT sector_name_unique IF NOT EXISTS FOR (s:Sector) REQUIRE s.sector_name IS UNIQUE;
CREATE CONSTRAINT location_name_unique IF NOT EXISTS FOR (l:Location) REQUIRE l.location_name IS UNIQUE;
