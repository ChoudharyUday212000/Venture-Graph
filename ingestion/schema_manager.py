"""
Neo4j schema and constraint management
Creates constraints, indexes, and validates graph schema
"""

from utils.logger import get_logger
from utils.errors import SchemaException
from ingestion.db_connection import Neo4jConnection
from config.neo4j_config import NODES_SCHEMA, RELATIONSHIPS_SCHEMA

logger = get_logger(__name__)


class SchemaManager:
    """Manages Neo4j schema creation and constraints"""

    @staticmethod
    def create_constraints() -> None:
        """Create unique constraints for all nodes"""
        logger.info("Creating unique constraints...")

        for node_label, schema in NODES_SCHEMA.items():
            primary_key = schema["primary_key"]
            constraint_name = f"{node_label}_{primary_key}_unique".lower()

            query = f"""
            CREATE CONSTRAINT {constraint_name}
            IF NOT EXISTS
            FOR (n:{node_label})
            REQUIRE n.{primary_key} IS UNIQUE
            """

            try:
                Neo4jConnection.execute_query(query, write_access=True)
                logger.info(f"[OK] Constraint created for {node_label}.{primary_key}")
            except Exception as e:
                if "already exists" in str(e).lower():
                    logger.info(f"  Constraint already exists for {node_label}.{primary_key}")
                else:
                    logger.warning(f"  Constraint creation note: {str(e)}")

    @staticmethod
    def create_indexes() -> None:
        """Create indexes for frequently queried properties"""
        logger.info("Creating indexes for query optimization...")

        indexes = [
            ("Company", "sector"),
            ("Company", "stage"),
            ("Company", "country"),
            ("Investor", "investor_type"),
            ("Investor", "hq_country"),
            ("Fund", "vintage"),
            ("Fund", "strategy"),
            ("Person", "role"),
        ]

        for node_label, property_name in indexes:
            index_name = f"idx_{node_label}_{property_name}".lower()
            query = f"""
            CREATE INDEX {index_name}
            IF NOT EXISTS
            FOR (n:{node_label})
            ON (n.{property_name})
            """

            try:
                Neo4jConnection.execute_query(query, write_access=True)
                logger.info(f"[OK] Index created: {node_label}.{property_name}")
            except Exception as e:
                if "already exists" in str(e).lower():
                    logger.info(f"  Index already exists: {node_label}.{property_name}")
                else:
                    logger.warning(f"  Index creation note: {str(e)}")

    @staticmethod
    def setup_schema() -> None:
        """Complete schema setup: constraints + indexes"""
        try:
            logger.info("=" * 60)
            logger.info("SETTING UP GRAPH SCHEMA")
            logger.info("=" * 60)

            SchemaManager.create_constraints()
            SchemaManager.create_indexes()

            logger.info("=" * 60)
            logger.info("[OK] Schema setup completed successfully")
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"✗ Schema setup failed: {str(e)}")
            raise SchemaException(f"Schema setup failed: {str(e)}")

    @staticmethod
    def clear_database(confirm: bool = False) -> None:
        """
        Clear all nodes and relationships from database
        Requires explicit confirmation to prevent accidental deletion
        """
        if not confirm:
            logger.warning("Database clear requires confirm=True parameter")
            return

        try:
            logger.warning("CLEARING ALL NODES AND RELATIONSHIPS...")
            Neo4jConnection.execute_query(
                "MATCH (n) DETACH DELETE n",
                write_access=True
            )
            logger.warning("[OK] Database cleared")
        except Exception as e:
            logger.error(f"✗ Failed to clear database: {str(e)}")
            raise SchemaException(f"Database clear failed: {str(e)}")

    @staticmethod
    def get_database_stats() -> dict:
        """Get current database statistics"""
        try:
            results = Neo4jConnection.execute_query("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(*) as count
                ORDER BY label
            """)

            stats = {"nodes": {}}
            for record in results:
                label = record["label"]
                count = record["count"]
                stats["nodes"][label] = count

            return stats
        except Exception as e:
            logger.error(f"Failed to get database stats: {str(e)}")
            return {}
