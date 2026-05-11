# AI Query Engine Changes

Added a new AI-powered natural language query module inside the existing Neo4j ingestion project.

## What changed

- Added `ai_query_engine/services/nl_to_cypher.py`
  - Loads the graph schema and prompt.
  - Calls OpenAI Responses API.
  - Returns only the generated Cypher text.

- Added `ai_query_engine/services/cypher_guard.py`
  - Blocks write/destructive Cypher.
  - Rejects semicolons and unsafe keywords.
  - Rejects `COMMITTED_TO`.
  - Adds `LIMIT 50` when missing.

- Added `ai_query_engine/services/query_executor.py`
  - Reuses `ingestion.db_connection.Neo4jConnection`.
  - Executes read-only queries with `write_access=False`.
  - Converts Neo4j records into JSON-safe dictionaries.

- Added `ai_query_engine/data/graph_schema.json`
  - Uses the existing graph schema.
  - Normalizes the relationship to `COMMITS_TO`.

- Added `ai_query_engine/prompts/cypher_prompt.txt`
  - Injects the schema dynamically.
  - Forces read-only, schema-bound Cypher.

- Added `app.py`
  - FastAPI app with `GET /ask?question=...`.
  - Serves the frontend at `/`.

- Added `static/index.html`
  - Minimal frontend with input box, Ask button, generated Cypher, and JSON results.

## Dependencies to install

```bash
pip install -r requirements.txt
```

## Environment variables

Set the existing Neo4j variables plus OpenAI:

```bash
NEO4J_URI=neo4j+s://your-db.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-5.4-mini
```

`OPENAI_MODEL` is optional. The code defaults to `gpt-5.4-mini`.

## Run

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## API examples

```text
GET http://127.0.0.1:8000/ask?question=Top%20investors%20by%20portfolio%20size
```

```text
GET http://127.0.0.1:8000/ask?question=Which%20funds%20invested%20in%20fintech%20companies
```

```text
GET http://127.0.0.1:8000/ask?question=Show%20companies%20operating%20in%20India
```

## Example Cypher the AI should produce

```cypher
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
RETURN i.name AS investor, count(DISTINCT c) AS portfolio_size
ORDER BY portfolio_size DESC
LIMIT 50
```

```cypher
MATCH (f:Fund)-[:INVESTED_IN]->(c:Company)
WHERE toLower(c.sector) CONTAINS "fintech"
RETURN DISTINCT f.name AS fund, c.name AS company
LIMIT 50
```

```cypher
MATCH (c:Company)
WHERE toLower(c.country) = "india"
RETURN c.name AS company, c.stage AS stage, c.sector AS sector
LIMIT 50
```
