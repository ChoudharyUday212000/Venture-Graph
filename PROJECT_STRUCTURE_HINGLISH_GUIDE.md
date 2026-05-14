# Project Structure Hinglish Guide

Ye file project structure ke hisab se explain karti hai ki kaunse folder/file me kya ho raha hai, aur runtime flow me woh file kis kaam aati hai.

## 1. Root folder

Project root:

```text
C:\Users\212627\Desktop\neo4j_project
```

Root level par main files:

```text
app.py
main.py
requirements.txt
.env
.gitignore
README_ETL.md
ARCHITECTURE.md
PROJECT_OVERVIEW.md
AI_QUERY_ENGINE_CHANGES.md
PROJECT_EXPLANATION_HINGLISH.md
```

### `app.py`

Ye AI web app ka main backend entry point hai.

Isme:

- FastAPI app create hoti hai.
- Browser UI serve hota hai.
- `/ask` endpoint create hota hai.
- User question ko OpenAI ke through Cypher me convert kiya jata hai.
- Generated Cypher ko safety guard se validate kiya jata hai.
- Neo4j par read-only query run hoti hai.
- Result browser ko return hota hai.

Main flow:

```text
Browser
  -> app.py /ask
  -> nl_to_cypher.py
  -> cypher_guard.py
  -> query_executor.py
  -> db_connection.py
  -> Neo4j
```

Run command:

```powershell
python app.py
```

### `main.py`

Ye original ETL project ka entry/helper file hai.

Iska use data ingestion, stats, validation jaise project operations ke liye hota hai. AI web app ke liye primary file `app.py` hai, lekin Neo4j graph prepare karne ke liye ETL pipeline important hai.

### `requirements.txt`

Ye dependencies list karta hai:

```text
neo4j
pandas
tqdm
fastapi
uvicorn
openai
```

Install:

```powershell
pip install -r requirements.txt
```

### `.env`

Ye local secrets/config file hai.

Isme Neo4j aur OpenAI credentials hote hain:

```env
NEO4J_URI=...
NEO4J_USERNAME=...
NEO4J_PASSWORD=...
OPENAI_API_KEY=...
OPENAI_MODEL=...
```

Important:

- Is file ko GitHub par push nahi karna.
- Placeholder values use nahi karni.
- Real OpenAI key aur real Neo4j URI required hai.

### `.gitignore`

Ye Git ko batata hai ki kaunsi files ignore karni hain.

Important ignored items:

- `.env`
- `.venv/`
- `__pycache__/`
- `logs/`

## 2. `config/` folder

Path:

```text
config/
```

Is folder ka kaam project configuration manage karna hai.

Files:

```text
config/__init__.py
config/neo4j_config.py
```

### `config/neo4j_config.py`

Ye config ka core file hai.

Isme:

- `.env` file load hoti hai.
- Neo4j URI, username, password read hota hai.
- Batch size define hota hai.
- Retry attempts define hote hain.
- Data folder paths define hote hain.
- Node CSV file mapping define hoti hai.
- Relationship CSV file mapping define hoti hai.
- Node schema define hota hai.
- Relationship schema define hota hai.
- Logging config define hoti hai.

Example responsibilities:

```text
NEO4J_URI
NEO4J_USERNAME
NEO4J_PASSWORD
NODE_FILES
RELATIONSHIP_FILES
NODES_SCHEMA
RELATIONSHIPS_SCHEMA
```

ETL pipeline aur DB connection dono is config ko use karte hain.

### `config/__init__.py`

Ye package export file hai.

Iska kaam hai `neo4j_config.py` ke important variables ko easy import ke liye expose karna.

Example:

```python
from config import NEO4J_URI, NODE_FILES
```

## 3. `data/` folder

Path:

```text
data/
```

Is folder me raw dataset aur Cypher scripts rakhe gaye hain.

Important files:

```text
companies.csv
investors.csv
funds.csv
people.csv
sectors.csv
locations.csv
company_located_in_location.csv
company_operates_in_sector.csv
fund_invested_in_company.csv
investor_manages_fund.csv
lp_commits_fund.csv
person_works_at_company.csv
person_works_for_investor.csv
person_board_member_company.csv
person_knows_person.csv
constraints.cypher
import.cypher
test_queries.cypher
graph_schema.json
synthetic_graph_dataset.json
README.md
```

### Node CSV files

Ye files graph ke nodes banati hain:

```text
companies.csv
investors.csv
funds.csv
people.csv
sectors.csv
locations.csv
```

Inse Neo4j me labels bante hain:

```text
Company
Investor
Fund
Person
Sector
Location
```

### Relationship CSV files

Ye files nodes ke beech relationships banati hain:

```text
company_located_in_location.csv
company_operates_in_sector.csv
fund_invested_in_company.csv
investor_manages_fund.csv
lp_commits_fund.csv
person_works_at_company.csv
person_works_for_investor.csv
person_board_member_company.csv
person_knows_person.csv
```

Inse Neo4j me relationships bante hain:

```text
LOCATED_IN
OPERATES_IN
INVESTED_IN
MANAGES
COMMITS_TO
WORKS_AT
WORKS_FOR
BOARD_MEMBER_OF
KNOWS
```

### `data/graph_schema.json`

Ye graph schema ka JSON version hai.

Use:

- Graph structure samajhne ke liye.
- AI prompt ko schema-aware banane ke liye reference.

### `data/constraints.cypher`

Neo4j constraints create karne ke Cypher statements.

Example purpose:

- Unique IDs enforce karna.
- Duplicate nodes avoid karna.

### `data/import.cypher`

Direct Cypher based import script.

Ye optional/alternate import approach ke liye use ho sakta hai.

### `data/test_queries.cypher`

Test queries rakhi gayi hain jisse graph load hone ke baad check kar sakein ki data sahi hai ya nahi.

## 4. `ingestion/` folder

Path:

```text
ingestion/
```

Ye ETL pipeline ka main folder hai.

Files:

```text
ingestion/__init__.py
ingestion/db_connection.py
ingestion/data_loader.py
ingestion/schema_manager.py
ingestion/node_ingestor.py
ingestion/relationship_ingestor.py
ingestion/etl_pipeline.py
```

### `ingestion/db_connection.py`

Neo4j database connection handle karta hai.

Isme:

- Neo4j driver create hota hai.
- Connection test hota hai.
- Query execute hoti hai.
- Retry logic use hota hai.
- Connection close hota hai.

Ye file ETL aur AI query app dono me use hoti hai.

Used by:

```text
ingestion/etl_pipeline.py
ai_query_engine/services/query_executor.py
queries/example_queries.py
```

### `ingestion/data_loader.py`

CSV data load karta hai.

Iska kaam:

- CSV files read karna.
- Required columns validate karna.
- DataFrame return karna.

Ye ETL pipeline ka first practical step hai.

### `ingestion/schema_manager.py`

Database schema create karta hai.

Iska kaam:

- Constraints create karna.
- Indexes create karna.
- Neo4j ko efficient aur consistent banana.

ETL run karne se pehle schema setup important hai.

### `ingestion/node_ingestor.py`

Nodes ingest karta hai.

Input:

- Node CSV files.
- Node schema.

Output:

- Neo4j me nodes create/merge.

Example:

```text
companies.csv -> (:Company)
investors.csv -> (:Investor)
funds.csv -> (:Fund)
```

### `ingestion/relationship_ingestor.py`

Relationships ingest karta hai.

Input:

- Relationship CSV files.
- Relationship schema.

Output:

- Neo4j me relationships create/merge.

Example:

```text
fund_invested_in_company.csv
  -> (:Fund)-[:INVESTED_IN]->(:Company)
```

### `ingestion/etl_pipeline.py`

Ye ETL ka orchestrator hai.

Iska kaam:

1. Neo4j connection initialize karna.
2. Schema constraints/indexes create karna.
3. Node ingestion run karna.
4. Relationship ingestion run karna.
5. Graph validation run karna.
6. Summary print/log karna.

Run:

```powershell
python ingestion/etl_pipeline.py
```

## 5. `ai_query_engine/` folder

Path:

```text
ai_query_engine/
```

Ye AI natural language query system ka folder hai.

Structure:

```text
ai_query_engine/
  __init__.py
  data/
    graph_schema.json
  prompts/
    cypher_prompt.txt
  services/
    __init__.py
    nl_to_cypher.py
    cypher_guard.py
    query_executor.py
```

### `ai_query_engine/data/graph_schema.json`

Ye AI engine ke liye schema file hai.

OpenAI ko batane ke liye use hota hai ki graph me kaunse nodes, relationships aur properties available hain.

Reason:

AI ko schema pata hoga to woh random query nahi banayega.

### `ai_query_engine/prompts/cypher_prompt.txt`

OpenAI ke liye prompt template.

Isme instructions hoti hain:

- Sirf Cypher return karo.
- Sirf read-only query banao.
- Schema ke bahar mat jao.
- Destructive query mat banao.
- `LIMIT 50` use karo.

### `ai_query_engine/services/nl_to_cypher.py`

Natural language question ko Cypher me convert karta hai.

Input:

```text
"Top investors by portfolio size"
```

Output:

```cypher
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
RETURN i.name AS investor, count(DISTINCT c) AS portfolio_size
ORDER BY portfolio_size DESC
LIMIT 50
```

Is file me:

- `.env` se OpenAI config load hota hai.
- Graph schema read hota hai.
- Prompt build hota hai.
- OpenAI API call hoti hai.
- Cypher text return hota hai.

### `ai_query_engine/services/cypher_guard.py`

Ye safety checker hai.

Iska kaam:

- AI generated Cypher ko validate karna.
- Unsafe keywords block karna.
- Write queries block karna.
- Missing `LIMIT` add karna.
- Only read queries allow karna.

Blocked examples:

```text
CREATE
MERGE
DELETE
SET
DROP
CALL
LOAD CSV
APOC
```

### `ai_query_engine/services/query_executor.py`

Validated Cypher ko Neo4j me execute karta hai.

Iska kaam:

- `Neo4jConnection.execute_query()` call karna.
- Read-only mode use karna.
- Neo4j result ko JSON-safe format me convert karna.

Ye API response ke liye result prepare karta hai.

## 6. `static/` folder

Path:

```text
static/
```

File:

```text
static/index.html
```

Ye browser UI hai.

UI me:

- Question input box.
- Ask button.
- Generated Cypher section.
- Results section.

JavaScript flow:

```text
User question type karta hai
  -> Ask button click
  -> fetch("/ask?question=...")
  -> response JSON parse
  -> Cypher aur result screen par show
```

Ye file `app.py` ke `/` route se serve hoti hai.

## 7. `queries/` folder

Path:

```text
queries/
```

Files:

```text
queries/example_queries.py
queries/analytics.cypher
queries/traversal.cypher
queries/visualization.cypher
```

### `queries/example_queries.py`

Python script hai jo sample queries run karta hai.

Use:

- Graph data test karna.
- Neo4j connection test karna.
- Example outputs dekhna.

### `queries/analytics.cypher`

Analytics queries rakhta hai.

Example use cases:

- Top investors.
- Sector-wise investment.
- Company/fund analytics.

### `queries/traversal.cypher`

Graph traversal queries.

Example:

- Investor se company tak path.
- Person network.
- Multi-hop relationships.

### `queries/visualization.cypher`

Neo4j Browser/Bloom visualization ke liye queries.

Use:

- Subgraph visualize karna.
- Relationship network dekhna.

## 8. `models/` folder

Path:

```text
models/
```

Files:

```text
models/__init__.py
models/graph_model.py
```

### `models/graph_model.py`

Python level graph entity models define karta hai.

Iska purpose:

- Data structure clear rakhna.
- Node/relationship representation standard karna.
- Type-level clarity provide karna.

## 9. `validation/` folder

Path:

```text
validation/
```

Files:

```text
validation/__init__.py
validation/graph_validator.py
```

### `validation/graph_validator.py`

Graph load hone ke baad validation karta hai.

Checks:

- Node counts.
- Relationship counts.
- Orphan nodes.
- Missing required relationships.
- Data integrity.

ETL ke baad ye confirm karne ke liye use hota hai ki graph correctly load hua ya nahi.

## 10. `utils/` folder

Path:

```text
utils/
```

Files:

```text
utils/__init__.py
utils/logger.py
utils/errors.py
```

### `utils/logger.py`

Logging setup karta hai.

Use:

- Console logs.
- File logs.
- Debugging.
- ETL progress tracking.

### `utils/errors.py`

Custom exceptions define karta hai.

Example:

- ConnectionException
- DataValidationException
- IngestionException

Custom errors se code readable aur maintainable rehta hai.

## 11. Documentation files

Project me multiple docs hain:

```text
README_ETL.md
ARCHITECTURE.md
PROJECT_OVERVIEW.md
PROJECT_STRUCTURE_THEORY_HINDI.md
AI_QUERY_ENGINE_CHANGES.md
PROJECT_EXPLANATION_HINGLISH.md
PROJECT_STRUCTURE_HINGLISH_GUIDE.md
```

### `README_ETL.md`

ETL system ka quick start aur overview.

### `ARCHITECTURE.md`

Technical architecture details.

### `PROJECT_OVERVIEW.md`

Project ka broader explanation.

### `PROJECT_STRUCTURE_THEORY_HINDI.md`

Hindi theory style explanation.

### `AI_QUERY_ENGINE_CHANGES.md`

AI query engine me kya add hua, uska summary.

### `PROJECT_EXPLANATION_HINGLISH.md`

Overall project ka detailed Hinglish explanation.

### `PROJECT_STRUCTURE_HINGLISH_GUIDE.md`

Ye current file hai. Isme project structure ke hisab se practical explanation hai.

## 12. ETL execution flow

Jab hum data Neo4j me load karte hain, flow kuchh aisa hota hai:

```text
python ingestion/etl_pipeline.py
  -> config/neo4j_config.py
  -> ingestion/db_connection.py
  -> ingestion/schema_manager.py
  -> ingestion/data_loader.py
  -> ingestion/node_ingestor.py
  -> ingestion/relationship_ingestor.py
  -> validation/graph_validator.py
  -> logs/
```

Detailed:

1. Config load hota hai.
2. Neo4j connection create hoti hai.
3. Constraints/indexes create hote hain.
4. CSV files read hoti hain.
5. Nodes create/merge hote hain.
6. Relationships create/merge hoti hain.
7. Graph validation hoti hai.
8. Logs generate hote hain.

## 13. AI app execution flow

Jab hum web app run karte hain:

```powershell
python app.py
```

Flow:

```text
app.py
  -> static/index.html
  -> /ask endpoint
  -> ai_query_engine/services/nl_to_cypher.py
  -> ai_query_engine/prompts/cypher_prompt.txt
  -> ai_query_engine/data/graph_schema.json
  -> OpenAI API
  -> ai_query_engine/services/cypher_guard.py
  -> ai_query_engine/services/query_executor.py
  -> ingestion/db_connection.py
  -> Neo4j
  -> JSON result
  -> static/index.html
```

Detailed:

1. Browser UI load hoti hai.
2. User question enter karta hai.
3. Frontend `/ask` API ko call karta hai.
4. Backend OpenAI ko schema ke saath prompt bhejta hai.
5. OpenAI Cypher query generate karta hai.
6. Safety guard query validate karta hai.
7. Query Neo4j par run hoti hai.
8. Result JSON me convert hota hai.
9. Browser me output show hota hai.

## 14. Kaunsi file kab use hoti hai

### App start karte time

```text
app.py
static/index.html
config/neo4j_config.py
```

### User question poochte time

```text
app.py
ai_query_engine/services/nl_to_cypher.py
ai_query_engine/prompts/cypher_prompt.txt
ai_query_engine/data/graph_schema.json
ai_query_engine/services/cypher_guard.py
ai_query_engine/services/query_executor.py
ingestion/db_connection.py
```

### Data load karte time

```text
ingestion/etl_pipeline.py
config/neo4j_config.py
ingestion/db_connection.py
ingestion/data_loader.py
ingestion/schema_manager.py
ingestion/node_ingestor.py
ingestion/relationship_ingestor.py
validation/graph_validator.py
data/*.csv
```

### Debugging karte time

```text
logs/
utils/logger.py
utils/errors.py
queries/example_queries.py
data/test_queries.cypher
```

## 15. Short mental model

Project ko aise samjho:

```text
data/ = raw data
config/ = settings and schema
ingestion/ = data ko Neo4j me daalne ka system
validation/ = load ke baad checking
queries/ = ready-made graph questions
ai_query_engine/ = natural language ko Cypher me convert karna
static/ = browser UI
app.py = AI app backend
utils/ = logging and errors
models/ = Python data models
```

## 16. Final simple summary

Is project me pehle hum CSV data ko Neo4j graph me load karte hain. Phir ek FastAPI app run karte hain jisme user browser se normal language me question poochta hai. Backend OpenAI se Cypher query generate karwata hai, safety guard se check karta hai, Neo4j par run karta hai, aur result frontend par show karta hai.

