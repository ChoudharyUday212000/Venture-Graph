# Neo4j Project Explanation - Hinglish

Ye file is project ka detailed Hinglish explanation hai. Isme hum explain kar rahe hain ki project ka purpose kya hai, kaun kaun se modules hain, data kaise Neo4j me load hota hai, AI query engine kaise kaam karta hai, app kaise run hoti hai, aur agar error aaye to kya check karna hai.

## 1. Project ka main purpose

Ye project ek Neo4j graph database based venture graph system hai.

Simple words me:

- Humare paas CSV files me companies, investors, funds, people, sectors, locations ka data hai.
- Hum is data ko Neo4j graph database me load karte hain.
- Neo4j me ye data nodes aur relationships ke form me store hota hai.
- Uske baad user natural language me question pooch sakta hai, jaise:
  - "Top investors by portfolio size"
  - "Show companies operating in India"
  - "Which funds invested in fintech companies"
- App OpenAI ka use karke natural language question ko Cypher query me convert karti hai.
- Cypher query safe hai ya nahi, ye validate hota hai.
- Safe query Neo4j database par run hoti hai.
- Result browser UI me JSON format me show hota hai.

Is project me do major parts hain:

1. ETL pipeline: CSV data ko Neo4j me load karna.
2. AI Query Engine: User question ko AI se Cypher me convert karke graph se answer nikalna.

## 2. Tech stack

Is project me ye technologies use ho rahi hain:

- Python: Backend logic, ETL pipeline, API server.
- Neo4j: Graph database.
- Cypher: Neo4j ki query language.
- FastAPI: Web API banane ke liye.
- Uvicorn: FastAPI app run karne ke liye ASGI server.
- OpenAI API: Natural language question ko Cypher query me convert karne ke liye.
- HTML, CSS, JavaScript: Simple frontend UI ke liye.
- CSV files: Source data ke liye.

## 3. Folder structure ka overview

Project root:

```text
neo4j_project/
```

Important files and folders:

```text
app.py
requirements.txt
.env
config/
ingestion/
ai_query_engine/
static/
data/
queries/
models/
validation/
utils/
```

### `app.py`

Ye FastAPI app ka main entry point hai.

Is file me:

- FastAPI app create hoti hai.
- Frontend `static/index.html` serve hota hai.
- `/ask` API endpoint define hota hai.
- User ka question receive hota hai.
- OpenAI se Cypher generate hota hai.
- Cypher validate hota hai.
- Query Neo4j par execute hoti hai.
- Result frontend ko return hota hai.

Main routes:

```text
GET /
GET /ask?question=...
```

### `requirements.txt`

Is file me Python dependencies hain:

```text
neo4j
pandas
tqdm
fastapi
uvicorn
openai
```

Inhe install karna zaroori hai:

```powershell
pip install -r requirements.txt
```

### `.env`

Ye local environment variables ke liye hai.

Important: Is file ko GitHub par push nahi karna chahiye, kyunki isme passwords aur API keys hoti hain.

Isme values kuchh is type ki honi chahiye:

```env
NEO4J_URI=neo4j+s://your-real-db.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-real-password
OPENAI_API_KEY=sk-your-real-openai-key
OPENAI_MODEL=gpt-5.4-mini
```

`OPENAI_API_KEY=your-openai-api-key` placeholder nahi chalega. Real API key lagani padegi.

## 4. Data model - Neo4j graph me kya store hota hai

Graph database me data nodes aur relationships me store hota hai.

### Nodes

Project me ye main node types hain:

- Company
- Investor
- Fund
- Person
- Sector
- Location

Example:

```text
(Company {name: "Example Startup"})
(Investor {name: "Example VC"})
(Fund {name: "Fund I"})
(Sector {sector_name: "Fintech"})
(Location {location_name: "India"})
```

### Relationships

Nodes ke beech relation banane ke liye relationships use hoti hain:

- `LOCATED_IN`: Company kis location me hai.
- `OPERATES_IN`: Company kis sector me kaam karti hai.
- `INVESTED_IN`: Fund ne kis company me invest kiya.
- `MANAGES`: Investor kaun sa fund manage karta hai.
- `COMMITS_TO`: Investor ne fund me commitment diya.
- `WORKS_AT`: Person kis company me kaam karta hai.
- `WORKS_FOR`: Person kis investor ke liye kaam karta hai.
- `BOARD_MEMBER_OF`: Person kis company ke board me hai.
- `KNOWS`: Ek person dusre person ko jaanta hai.

Example graph relation:

```cypher
(Investor)-[:MANAGES]->(Fund)-[:INVESTED_IN]->(Company)
```

Iska meaning:

Investor fund manage karta hai, aur fund company me invest karta hai.

## 5. ETL pipeline me hum kya kar rahe hain

ETL ka full form hai:

```text
Extract - Transform - Load
```

Is project me:

1. Extract: CSV files se data read hota hai.
2. Transform: Data validate aur prepare hota hai.
3. Load: Data Neo4j database me nodes/relationships ke form me insert hota hai.

### ETL files

Important ETL files:

```text
ingestion/db_connection.py
ingestion/data_loader.py
ingestion/schema_manager.py
ingestion/node_ingestor.py
ingestion/relationship_ingestor.py
ingestion/etl_pipeline.py
```

### `ingestion/db_connection.py`

Ye Neo4j connection manage karta hai.

Responsibilities:

- Neo4j driver create karna.
- `.env` se URI, username, password lena.
- Query execute karna.
- Retry logic handle karna.
- Connection close karna.

### `ingestion/data_loader.py`

Ye CSV files load karta hai.

Responsibilities:

- `data/` folder se CSV read karna.
- Required columns validate karna.
- Data ko pandas DataFrame me convert karna.

### `ingestion/schema_manager.py`

Ye Neo4j schema setup karta hai.

Responsibilities:

- Unique constraints create karna.
- Indexes create karna.
- Database ko efficient query ke liye prepare karna.

### `ingestion/node_ingestor.py`

Ye nodes create karta hai.

Example:

- Company nodes
- Investor nodes
- Fund nodes
- Person nodes
- Sector nodes
- Location nodes

Ye mostly `MERGE` use karta hai, taaki duplicate nodes create na ho.

### `ingestion/relationship_ingestor.py`

Ye relationships create karta hai.

Example:

- Company to Sector
- Company to Location
- Fund to Company investment
- Investor to Fund management
- Person to Company employment

### `ingestion/etl_pipeline.py`

Ye poori ETL process orchestrate karta hai.

Typical flow:

1. Neo4j connection initialize.
2. Constraints/indexes create.
3. Nodes ingest.
4. Relationships ingest.
5. Graph validate.
6. Summary logs generate.

Run command:

```powershell
python ingestion/etl_pipeline.py
```

## 6. AI Query Engine me hum kya kar rahe hain

AI Query Engine ka kaam hai user ke English/Hinglish natural language question ko Neo4j Cypher query me convert karna.

Example:

User input:

```text
Top investors by portfolio size
```

AI generated Cypher:

```cypher
MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
RETURN i.name AS investor, count(DISTINCT c) AS portfolio_size
ORDER BY portfolio_size DESC
LIMIT 50
```

Phir ye Cypher Neo4j par run hoti hai aur result frontend par show hota hai.

### AI Query Engine folder

```text
ai_query_engine/
  data/
  prompts/
  services/
```

### `ai_query_engine/data/graph_schema.json`

Is file me graph ka schema hai.

Schema batata hai:

- Kaun se node labels allowed hain.
- Kaun se relationships allowed hain.
- Kaun si properties available hain.

OpenAI prompt me ye schema inject hota hai, taaki model random ya wrong Cypher na banaye.

### `ai_query_engine/prompts/cypher_prompt.txt`

Ye prompt template hai jo OpenAI ko instructions deta hai.

Prompt ka goal:

- Sirf read-only Cypher generate karna.
- Sirf available schema use karna.
- `MATCH`, `OPTIONAL MATCH`, `RETURN`, `LIMIT` wali query banana.
- Destructive commands avoid karna.
- Extra explanation na dena, sirf Cypher dena.

### `ai_query_engine/services/nl_to_cypher.py`

Ye natural language to Cypher conversion karta hai.

Flow:

1. `.env` se OpenAI API key load karta hai.
2. Graph schema read karta hai.
3. Prompt build karta hai.
4. OpenAI Responses API call karta hai.
5. Generated Cypher return karta hai.
6. Agar generated Cypher invalid ho to retry prompt use karta hai.

Important:

- Agar `OPENAI_API_KEY` missing ho, app error degi.
- Agar placeholder key ho, app error degi.
- Real OpenAI key required hai.

### `ai_query_engine/services/cypher_guard.py`

Ye safety layer hai.

AI kabhi kabhi unsafe query generate kar sakta hai. Isliye hum query ko directly Neo4j par nahi chalate.

Guard check karta hai:

- Query empty na ho.
- Query `MATCH`, `OPTIONAL MATCH`, ya `WITH` se start ho.
- Query me semicolon na ho.
- Query me write/destructive keywords na ho.
- Query me `CREATE`, `MERGE`, `DELETE`, `SET`, `REMOVE`, `DROP`, `CALL`, `LOAD CSV`, `APOC` jaise keywords na ho.
- Query me `RETURN` ho.
- Query me `LIMIT` na ho to default `LIMIT 50` add ho.

Isse database safe rehta hai.

### `ai_query_engine/services/query_executor.py`

Ye validated Cypher ko Neo4j par execute karta hai.

Responsibilities:

- Existing `Neo4jConnection` reuse karna.
- Query read-only mode me chalana.
- Neo4j records ko JSON-safe dictionary me convert karna.
- Nodes, relationships, lists, dicts ko frontend friendly format me convert karna.

## 7. Frontend me kya ho raha hai

Frontend file:

```text
static/index.html
```

Isme simple UI hai:

- Question input box
- Ask button
- Generated Cypher display area
- Results display area

Frontend flow:

1. User question type karta hai.
2. Ask button click karta hai.
3. JavaScript `/ask?question=...` API call karta hai.
4. Backend response me `cypher` aur `result` bhejta hai.
5. UI generated Cypher aur JSON result show karta hai.

## 8. Full request flow end to end

Ye complete flow hai jab user browser me question poochta hai:

1. Browser open hota hai:

```text
http://127.0.0.1:8000/
```

2. `static/index.html` load hota hai.

3. User input deta hai:

```text
Show companies operating in India
```

4. Frontend request bhejta hai:

```text
GET /ask?question=Show%20companies%20operating%20in%20India
```

5. `app.py` ka `/ask` endpoint call hota hai.

6. `generate_cypher(question)` call hota hai.

7. OpenAI model question aur schema ke basis par Cypher generate karta hai.

8. `validate_and_prepare_cypher()` query ko safe check karta hai.

9. `execute_read_query()` Neo4j par query run karta hai.

10. Neo4j result return karta hai.

11. Backend JSON response bhejta hai:

```json
{
  "question": "Show companies operating in India",
  "cypher": "MATCH ... RETURN ... LIMIT 50",
  "result": []
}
```

12. Frontend result show karta hai.

## 9. App run karne ke steps

PowerShell open karo.

Project folder me jao:

```powershell
cd C:\Users\212627\Desktop\neo4j_project
```

Virtual environment activate karo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Agar activation policy error aaye:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Phir dobara activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Dependencies install karo:

```powershell
pip install -r requirements.txt
```

`.env` file check karo:

```env
NEO4J_URI=neo4j+s://your-real-database-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-real-password
OPENAI_API_KEY=sk-your-real-openai-key
OPENAI_MODEL=gpt-5.4-mini
```

App run karo:

```powershell
python app.py
```

Browser me open karo:

```text
http://127.0.0.1:8000/
```

Agar port 8000 busy ho:

```powershell
$env:PORT="8001"
python app.py
```

Browser me open karo:

```text
http://127.0.0.1:8001/
```

## 10. API direct test kaise karein

Browser ya PowerShell se test:

```text
http://127.0.0.1:8000/ask?question=List%205%20companies
```

PowerShell:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/ask?question=List%205%20companies" -UseBasicParsing
```

## 11. Common errors aur meaning

### Error: Incorrect API key provided

Example:

```text
OpenAI Cypher generation failed: Error code: 401
```

Meaning:

`OPENAI_API_KEY` galat hai ya placeholder hai.

Fix:

`.env` me real OpenAI API key lagao:

```env
OPENAI_API_KEY=sk-your-real-key
```

Server restart karo.

### Error: Neo4j DNS resolve failed

Example:

```text
Failed to DNS resolve address 0674b566.databases.neo4j.io:7687
```

Meaning:

Machine Neo4j Aura host ko resolve nahi kar paa rahi.

Possible reasons:

- `NEO4J_URI` galat hai.
- Neo4j Aura database stopped/paused/deleted hai.
- Internet/DNS issue hai.
- Corporate firewall/VPN port 7687 block kar raha hai.
- Aura database ka host ID wrong hai.

Fix:

1. Neo4j Aura dashboard open karo.
2. Database running hai ya nahi check karo.
3. Correct connection URI copy karo.
4. `.env` me `NEO4J_URI` update karo.
5. Internet/VPN/firewall check karo.
6. App restart karo.

### Error: Port already in use

Meaning:

Port 8000 par pehle se server chal raha hai.

Fix:

Option 1: Running server terminal me `Ctrl + C`.

Option 2: Different port use karo:

```powershell
$env:PORT="8001"
python app.py
```

### Error: Placeholder OpenAI key

Agar `.env` me ye hai:

```env
OPENAI_API_KEY=your-openai-api-key
```

To app kaam nahi karegi.

Real key required hai.

## 12. Current important note

Recent end-to-end check me:

- Frontend load ho raha tha.
- OpenAI call successful tha.
- Main blocker Neo4j DNS tha.

Issue:

```text
0674b566.databases.neo4j.io resolve nahi ho raha tha
```

Iska matlab app ka code basic level par chal raha hai, lekin database connection complete nahi ho paa raha. Jab tak Neo4j URI/network fix nahi hota, `/ask` endpoint generated Cypher ke baad Neo4j result nahi laa paayega.

## 13. Security points

Important security rules:

- `.env` GitHub par push nahi karna.
- OpenAI API key public nahi karni.
- Neo4j password public nahi karna.
- AI generated query ko directly execute nahi karna.
- `cypher_guard.py` jaisi safety layer zaroor use karni.
- Write queries block karni chahiye.

## 14. Is project me humne kya add kiya

Existing project me ETL already tha. Humne AI app layer add ki:

- FastAPI backend.
- Browser frontend.
- OpenAI natural language to Cypher conversion.
- Cypher safety guard.
- Neo4j read query executor.
- Graph schema based prompt.
- Environment variable loading for OpenAI.
- Placeholder API key detection.
- Timeout improvements for external calls.

## 15. Final summary

Ye project ek complete graph + AI query system hai.

High-level flow:

```text
CSV Data
  -> ETL Pipeline
  -> Neo4j Graph Database
  -> FastAPI App
  -> User Question
  -> OpenAI generates Cypher
  -> Safety Guard validates Cypher
  -> Neo4j executes read query
  -> Browser shows answer
```

Short me:

Hum CSV data ko Neo4j graph me daal rahe hain, phir ek AI-powered web app bana rahe hain jisme user normal language me question pooch sakta hai, aur backend OpenAI + Cypher + Neo4j use karke answer nikalta hai.

