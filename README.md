# Venture Capital Graph + AI Query Engine

A Python and Neo4j project for ingesting venture-capital data as a graph, validating its relationships, and exploring the graph with natural-language questions converted into read-only Cypher queries.

## What it demonstrates

- ETL of CSV datasets into Neo4j nodes and relationships
- A schema-driven graph model with constraints and relationship properties
- Batch ingestion and graph-integrity validation
- Graph analytics and traversal queries
- A FastAPI UI/API that uses an OpenAI model to draft Cypher, validates the generated query, and executes it in read-only mode

## Architecture

~~~text
CSV datasets
    |
    v
Data loading and validation
    |
    v
Schema manager + node / relationship ingestion
    |
    v
Neo4j graph
    |
    +----> Traversal and analytics queries
    |
    +----> Natural-language question
                |
                v
          OpenAI Cypher generation
                |
                v
          Cypher validation guard
                |
                v
          Read-only query executor
                |
                v
          JSON response / browser UI
~~~

## Graph model

Current model definitions include:

- Nodes: Company, Investor, Fund, Person, Sector and Location.
- Relationships: INVESTED_IN, MANAGES, COMMITS_TO, WORKS_AT, WORKS_FOR, BOARD_MEMBER_OF, KNOWS, LOCATED_IN and OPERATES_IN.
- Investment relationships can carry round, year and amount properties.
- CSV data and schema definitions live in the data directory.

## Technology

Python · Neo4j · FastAPI · Uvicorn · Pandas · OpenAI Responses API

## Setup

Requirements: Python 3.10+ and a Neo4j database (Neo4j Aura is supported).

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
~~~

On Windows PowerShell, activate the environment with .venv\Scripts\Activate.ps1.

Edit the local .env file with your own credentials:

~~~dotenv
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=replace-with-your-password
OPENAI_API_KEY=replace-with-your-api-key
OPENAI_MODEL=gpt-5.4-mini
~~~

Never commit .env or credentials. OPENAI_MODEL is optional; the query module has a default model.

## Run the ETL workflow

~~~bash
python main.py
~~~

The command-line menu can run the ingestion pipeline, clear and reload the graph (destructive), show graph statistics, or validate graph integrity. Review the selected environment and database before choosing the clear-and-reload option.

## Run the natural-language query API

~~~bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
~~~

Open http://127.0.0.1:8000 for the browser UI. API documentation is available from FastAPI at /docs while the application is running.

Example request:

~~~bash
curl --get 'http://127.0.0.1:8000/ask' \
  --data-urlencode 'question=Which funds invested in fintech companies?'
~~~

The response includes the submitted question, the validated Cypher query and JSON-safe result rows.

## Safety and limitations

The query path uses a schema-aware prompt, a read-only query guard and a read-only Neo4j execution call. This is defense in depth, not a complete security boundary: a regex-based Cypher validator is not a substitute for database least-privilege credentials, query timeouts, request limits and adversarial testing. Use a dedicated read-only Neo4j account for the AI query API. Do not expose it publicly without authentication, rate limiting, observability and stronger query-policy testing.

The included data may be synthetic/sample data. Verify provenance and schema assumptions before using it for business decisions. Model-generated Cypher can be incorrect even when syntactically valid.

## Repository map

- ingestion/: ETL, database connection, schema management and node/relationship loaders
- validation/: graph-integrity checks
- queries/: analytics, traversal and visualization examples
- ai_query_engine/: prompts, schema and guarded natural-language query flow
- static/: browser UI
- data/: sample CSV data and Cypher setup/query scripts
- main.py: interactive ETL entry point
- app.py: FastAPI query application
