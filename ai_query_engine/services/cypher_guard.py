"""Safety checks for AI-generated Cypher before execution."""

import re


FORBIDDEN_KEYWORDS = (
    "CREATE",
    "MERGE",
    "DELETE",
    "SET",
    "REMOVE",
    "DROP",
    "CALL",
    "LOAD CSV",
    "APOC",
    "UNION",
    "UNWIND",
    "FOREACH",
    "DETACH",
    "ALTER",
    "GRANT",
    "DENY",
    "REVOKE",
)

ALLOWED_STARTS = ("MATCH", "OPTIONAL MATCH", "WITH")
DEFAULT_LIMIT = 50


class CypherValidationError(ValueError):
    """Raised when a Cypher query is unsafe or invalid."""


def validate_and_prepare_cypher(cypher: str, default_limit: int = DEFAULT_LIMIT) -> str:
    """
    Validate AI-generated Cypher and add a default LIMIT when missing.

    The guard intentionally keeps rules simple and strict because generated
    queries must never reach Neo4j until they pass read-only validation.
    """
    if not cypher or not cypher.strip():
        raise CypherValidationError("Cypher query is empty.")

    cleaned = _strip_code_fences(cypher).strip()
    upper_query = cleaned.upper()

    if ";" in cleaned:
        raise CypherValidationError("Semicolons and multiple statements are not allowed.")

    if not upper_query.startswith(ALLOWED_STARTS):
        raise CypherValidationError("Only read-only MATCH/OPTIONAL MATCH/WITH queries are allowed.")

    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"(?<![A-Z0-9_]){re.escape(keyword)}(?![A-Z0-9_])"
        if re.search(pattern, upper_query):
            raise CypherValidationError(f"Forbidden Cypher keyword found: {keyword}")

    if "COMMITTED_TO" in upper_query:
        raise CypherValidationError("Use COMMITS_TO relationship, not COMMITTED_TO.")

    if not re.search(r"(?<![A-Z0-9_])RETURN(?![A-Z0-9_])", upper_query):
        raise CypherValidationError("Read-only queries must include RETURN.")

    if not re.search(r"(?<![A-Z0-9_])LIMIT\s+\d+(?![A-Z0-9_])", upper_query):
        cleaned = f"{cleaned}\nLIMIT {default_limit}"

    return cleaned


def _strip_code_fences(value: str) -> str:
    """Handle occasional fenced output from a model before strict validation."""
    stripped = value.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:cypher)?\s*", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()
