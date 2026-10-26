import pytest

from ai_query_engine.services.cypher_guard import (
    CypherValidationError,
    validate_and_prepare_cypher,
)


def test_adds_default_limit_to_read_only_query():
    query = validate_and_prepare_cypher("MATCH (c:Company) RETURN c.name AS company")
    assert query.endswith("LIMIT 50")


def test_preserves_explicit_limit():
    query = "MATCH (c:Company) RETURN c.name AS company LIMIT 7"
    assert validate_and_prepare_cypher(query) == query


def test_accepts_optional_match_read_query():
    query = "OPTIONAL MATCH (i:Investor) RETURN i.name AS investor LIMIT 10"
    assert validate_and_prepare_cypher(query) == query


def test_strips_cypher_markdown_fences():
    query = validate_and_prepare_cypher(
        "```cypher\nMATCH (c:Company) RETURN c.name\n```"
    )
    assert query.startswith("MATCH ")
    assert query.endswith("LIMIT 50")


@pytest.mark.parametrize(
    "query",
    [
        "CREATE (c:Company {name: 'unsafe'}) RETURN c",
        "MATCH (c:Company) DETACH DELETE c RETURN c",
        "MATCH (c:Company); MATCH (i:Investor) RETURN i",
        "MATCH (c:Company) RETURN c COMMITTED_TO",
        "RETURN 1",
        "",
        "   ",
    ],
)
def test_rejects_unsafe_or_incomplete_queries(query):
    with pytest.raises(CypherValidationError):
        validate_and_prepare_cypher(query)


def test_rejects_write_keyword_even_inside_a_read_query():
    with pytest.raises(CypherValidationError, match="Forbidden Cypher keyword"):
        validate_and_prepare_cypher(
            "MATCH (c:Company) WITH c AS company DELETE company RETURN company"
        )
