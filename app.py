"""FastAPI app for asking natural language questions against the Neo4j graph."""

import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from ai_query_engine.services.cypher_guard import (  # noqa: E402
    CypherValidationError,
    validate_and_prepare_cypher,
)
from ai_query_engine.services.nl_to_cypher import (  # noqa: E402
    CypherGenerationError,
    generate_cypher,
)
from ai_query_engine.services.query_executor import execute_read_query  # noqa: E402
from ingestion.db_connection import Neo4jConnection  # noqa: E402


app = FastAPI(title="Neo4j AI Query Engine", version="1.0.0")
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")


@app.on_event("startup")
def startup() -> None:
    # Neo4j is initialized lazily when a query runs. This keeps the UI available
    # while users are still fixing .env credentials.
    pass


@app.on_event("shutdown")
def shutdown() -> None:
    Neo4jConnection.close()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(ROOT_DIR / "static" / "index.html")


@app.get("/ask")
def ask(question: str = Query(..., min_length=1)) -> dict:
    try:
        generated_cypher = generate_cypher(question)
        safe_cypher = validate_and_prepare_cypher(generated_cypher)
        result = execute_read_query(safe_cypher)

        return {
            "question": question,
            "cypher": safe_cypher,
            "result": result,
        }
    except (CypherGenerationError, CypherValidationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query failed: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)
