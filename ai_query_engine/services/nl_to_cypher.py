"""Convert natural language questions into safe Cypher candidates with OpenAI."""

import json
import os
from pathlib import Path

from openai import OpenAI

from ai_query_engine.services.cypher_guard import validate_and_prepare_cypher


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent
SCHEMA_PATH = BASE_DIR / "data" / "graph_schema.json"
PROMPT_PATH = BASE_DIR / "prompts" / "cypher_prompt.txt"
DEFAULT_MODEL = "gpt-5.4-mini"


class CypherGenerationError(RuntimeError):
    """Raised when Cypher generation fails."""


def generate_cypher(question: str) -> str:
    """Generate a Cypher query from a natural language question."""
    if not question or not question.strip():
        raise CypherGenerationError("Question cannot be empty.")

    try:
        _load_openai_env()
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key or _looks_like_placeholder(api_key):
            raise CypherGenerationError(
                "OPENAI_API_KEY is missing or still has the placeholder value."
            )

        client = OpenAI(api_key=api_key, timeout=20.0, max_retries=0)
        prompt = _build_prompt(question.strip())
        model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

        response = client.responses.create(model=model, input=prompt, max_output_tokens=600)
        cypher = response.output_text.strip()

        try:
            validate_and_prepare_cypher(cypher)
        except Exception:
            retry_prompt = (
                f"{prompt}\n\n"
                "The previous answer was invalid. Return exactly one read-only Cypher "
                "query with MATCH or OPTIONAL MATCH, RETURN, and LIMIT 50."
            )
            response = client.responses.create(
                model=model,
                input=retry_prompt,
                max_output_tokens=600,
            )
            cypher = response.output_text.strip()

        return cypher
    except Exception as exc:
        raise CypherGenerationError(f"OpenAI Cypher generation failed: {exc}") from exc


def _build_prompt(question: str) -> str:
    schema = _load_schema()
    template = PROMPT_PATH.read_text(encoding="utf-8")
    return template.format(schema=json.dumps(schema, indent=2), question=question)


def _load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)

    relationships = schema.get("relationship_types", {})
    relationships.pop("COMMITTED_TO", None)
    if "COMMITS_TO" not in relationships:
        relationships["COMMITS_TO"] = {
            "from": "Investor",
            "to": "Fund",
            "properties": ["commitment_usd", "year"],
        }
    return schema


def _load_openai_env() -> None:
    """
    Load OpenAI settings from the project .env file.

    The existing config loader keeps pre-existing environment variables. For
    OpenAI, we replace obvious placeholder values so a stale shell variable like
    OPENAI_API_KEY=your_openai_api_key does not break the running API server.
    """
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key not in {"OPENAI_API_KEY", "OPENAI_MODEL"}:
            continue

        current_value = os.getenv(key, "")
        if key == "OPENAI_API_KEY" and value and not _looks_like_placeholder(value):
            os.environ[key] = value
        elif not current_value or _looks_like_placeholder(current_value):
            os.environ[key] = value


def _looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().lower().replace("-", "_")
    return normalized.startswith("your_") or "your_openai" in normalized
