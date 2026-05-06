"""
Neo4j database connection management
Handles driver creation, connection pooling, and lifecycle
"""

from neo4j import GraphDatabase, Driver
from typing import Optional, Callable, Any
import time
from utils.logger import get_logger
from utils.errors import ConnectionException
from config.neo4j_config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    RETRY_ATTEMPTS,
    RETRY_DELAY,
)

logger = get_logger(__name__)


class Neo4jConnection:
    """Manages Neo4j database connection"""

    _instance: Optional[Driver] = None
    _initialized: bool = False

    @classmethod
    def initialize(cls) -> Driver:
        """Initialize or get existing Neo4j driver"""
        if cls._instance is None or not cls._initialized:
            cls._instance = cls._create_driver()
            cls._initialized = True
        return cls._instance

    @classmethod
    def _create_driver(cls) -> Driver:
        """Create Neo4j driver with error handling"""
        try:
            logger.info(f"Connecting to Neo4j at {NEO4J_URI}...")
            driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
            )
            # Test connection
            with driver.session() as session:
                session.run("RETURN 'Neo4j Connection Successful' AS msg")
            logger.info("[OK] Neo4j connection established successfully")
            return driver
        except Exception as e:
            logger.error(f"✗ Failed to connect to Neo4j: {str(e)}")
            raise ConnectionException(f"Cannot connect to Neo4j: {str(e)}")

    @classmethod
    def get_driver(cls) -> Driver:
        """Get the Neo4j driver instance"""
        if cls._instance is None:
            return cls.initialize()
        return cls._instance

    @classmethod
    def close(cls) -> None:
        """Close Neo4j driver connection"""
        if cls._instance is not None:
            cls._instance.close()
            cls._initialized = False
            logger.info("Neo4j connection closed")

    @classmethod
    def execute_query(
        cls, query: str, parameters: Optional[dict] = None, write_access: bool = False
    ) -> list:
        """
        Execute a Cypher query with retry logic

        Args:
            query: Cypher query string
            parameters: Query parameters
            write_access: If True, uses write session; else uses read session

        Returns:
            List of result records
        """
        driver = cls.get_driver()
        parameters = parameters or {}

        for attempt in range(RETRY_ATTEMPTS):
            try:
                with driver.session() as session:
                    if write_access:
                        result = session.execute_write(
                            lambda tx: list(tx.run(query, parameters))
                        )
                    else:
                        result = session.execute_read(
                            lambda tx: list(tx.run(query, parameters))
                        )
                    return result
            except Exception as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    logger.warning(
                        f"Query failed (attempt {attempt + 1}/{RETRY_ATTEMPTS}): {str(e)}. Retrying..."
                    )
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Query failed after {RETRY_ATTEMPTS} attempts: {str(e)}")
                    raise

    @classmethod
    def execute_transaction(cls, func: Callable, write_access: bool = False) -> Any:
        """Execute a transaction with custom logic"""
        driver = cls.get_driver()

        with driver.session() as session:
            if write_access:
                return session.execute_write(func)
            else:
                return session.execute_read(func)
