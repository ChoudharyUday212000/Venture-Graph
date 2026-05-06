# Neo4j Starter Package

This bundle contains a small synthetic graph for testing Neo4j with companies, investors (GPs and LPs), funds, and people.

## Files
- graph_schema.json: Practical ontology/schema
- synthetic_graph_dataset.json: Human-readable master dataset
- CSV files: Node and relationship files for import
- constraints.cypher: Uniqueness constraints
- import.cypher: LOAD CSV import script
- test_queries.cypher: Sample multi-hop queries

## Recommended import flow
1. Copy the CSV files into your Neo4j import directory.
2. Run constraints.cypher.
3. Run import.cypher.
4. Run test_queries.cypher.

## Entity counts
- Companies: 10
- Investors: 8 (4 GPs, 4 LPs)
- Funds: 6
- People: 20

## Notes
- IDs are synthetic and deterministic: C1..C10, I1..I8, F1..F6, P1..P20.
- The graph intentionally includes multi-hop paths like LP -> Fund -> Company and Person -> Investor -> Fund -> Company.
