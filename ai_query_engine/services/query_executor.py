"""Execute validated read-only Cypher using the existing Neo4j connection."""

from typing import Any

from ingestion.db_connection import Neo4jConnection


def execute_read_query(cypher: str) -> list[dict[str, Any]]:
    """Run a safe read-only query and return JSON-serializable rows."""
    records = Neo4jConnection.execute_query(cypher, write_access=False)
    return [_record_to_dict(record) for record in records]


def _record_to_dict(record: Any) -> dict[str, Any]:
    return {key: _to_json_safe(record[key]) for key in record.keys()}


def _to_json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, list):
        return [_to_json_safe(item) for item in value]

    if isinstance(value, tuple):
        return [_to_json_safe(item) for item in value]

    if isinstance(value, dict):
        return {str(key): _to_json_safe(item) for key, item in value.items()}

    if hasattr(value, "items"):
        return {str(key): _to_json_safe(item) for key, item in value.items()}

    if hasattr(value, "_properties"):
        data = dict(value._properties)
        if hasattr(value, "labels"):
            data["_labels"] = sorted(value.labels)
        if hasattr(value, "type"):
            data["_type"] = value.type
        return _to_json_safe(data)

    return str(value)
