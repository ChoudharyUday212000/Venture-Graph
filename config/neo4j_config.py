"""
Neo4j Aura Configuration Module
Centralizes all connection and environment settings
"""

import os
from typing import Dict, Any


def _load_local_env() -> None:
    """Load simple KEY=VALUE pairs from a local .env file if present."""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_local_env()

# Neo4j Connection Settings
# Set these in your shell or a local .env file before running the ETL.
NEO4J_URI = os.getenv("NEO4J_URI", "")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")

# ETL Configuration
BATCH_SIZE = 100
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds
TRANSACTION_TIMEOUT = 60  # seconds

# File Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
QUERY_DIR = os.path.join(os.path.dirname(__file__), "..", "queries")

# Node Files
NODE_FILES = {
    "Company": "companies.csv",
    "Investor": "investors.csv",
    "Fund": "funds.csv",
    "Person": "people.csv",
    "Sector": "sectors.csv",
    "Location": "locations.csv",
}

# Relationship Files
RELATIONSHIP_FILES = {
    "LOCATED_IN": "company_located_in_location.csv",
    "OPERATES_IN": "company_operates_in_sector.csv",
    "INVESTED_IN": "fund_invested_in_company.csv",
    "MANAGES": "investor_manages_fund.csv",
    "COMMITS_TO": "lp_commits_fund.csv",
    "WORKS_AT": "person_works_at_company.csv",
    "WORKS_FOR": "person_works_for_investor.csv",
    "BOARD_MEMBER_OF": "person_board_member_company.csv",
    "KNOWS": "person_knows_person.csv",
}

# Graph Schema - Node Definitions
NODES_SCHEMA: Dict[str, Dict[str, Any]] = {
    "Company": {
        "label": "Company",
        "primary_key": "company_id",
        "properties": ["company_id", "name", "sector", "stage", "country"],
        "unique_constraints": ["company_id"],
    },
    "Investor": {
        "label": "Investor",
        "primary_key": "investor_id",
        "properties": ["investor_id", "name", "investor_type", "hq_country"],
        "unique_constraints": ["investor_id"],
    },
    "Fund": {
        "label": "Fund",
        "primary_key": "fund_id",
        "properties": ["fund_id", "name", "vintage", "strategy"],
        "unique_constraints": ["fund_id"],
    },
    "Person": {
        "label": "Person",
        "primary_key": "person_id",
        "properties": ["person_id", "name", "role"],
        "unique_constraints": ["person_id"],
    },
    "Sector": {
        "label": "Sector",
        "primary_key": "sector_name",
        "properties": ["sector_name"],
        "unique_constraints": ["sector_name"],
    },
    "Location": {
        "label": "Location",
        "primary_key": "location_name",
        "properties": ["location_name"],
        "unique_constraints": ["location_name"],
    },
}

# Graph Schema - Relationship Definitions
RELATIONSHIPS_SCHEMA: Dict[str, Dict[str, Any]] = {
    "LOCATED_IN": {
        "type": "LOCATED_IN",
        "from_node": "Company",
        "to_node": "Location",
        "properties": [],
        "cardinality": "many-to-one",
    },
    "OPERATES_IN": {
        "type": "OPERATES_IN",
        "from_node": "Company",
        "to_node": "Sector",
        "properties": [],
        "cardinality": "many-to-one",
    },
    "INVESTED_IN": {
        "type": "INVESTED_IN",
        "from_node": "Fund",
        "to_node": "Company",
        "properties": ["round", "year", "amount_usd"],
        "cardinality": "many-to-many",
    },
    "MANAGES": {
        "type": "MANAGES",
        "from_node": "Investor",
        "to_node": "Fund",
        "properties": [],
        "cardinality": "many-to-many",
    },
    "COMMITS_TO": {
        "type": "COMMITS_TO",
        "from_node": "Investor",
        "to_node": "Fund",
        "properties": ["commitment_usd", "year"],
        "cardinality": "many-to-many",
    },
    "WORKS_AT": {
        "type": "WORKS_AT",
        "from_node": "Person",
        "to_node": "Company",
        "properties": ["title"],
        "cardinality": "many-to-many",
    },
    "WORKS_FOR": {
        "type": "WORKS_FOR",
        "from_node": "Person",
        "to_node": "Investor",
        "properties": ["title"],
        "cardinality": "many-to-many",
    },
    "BOARD_MEMBER_OF": {
        "type": "BOARD_MEMBER_OF",
        "from_node": "Person",
        "to_node": "Company",
        "properties": ["since_year"],
        "cardinality": "many-to-many",
    },
    "KNOWS": {
        "type": "KNOWS",
        "from_node": "Person",
        "to_node": "Person",
        "properties": ["strength"],
        "cardinality": "many-to-many",
    },
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": os.path.join(LOG_DIR, "neo4j_etl.log"),
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        }
    },
}
