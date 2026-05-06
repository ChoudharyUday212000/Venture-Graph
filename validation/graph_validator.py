"""
Graph validation module
Validates data integrity and graph consistency
"""

from utils.logger import get_logger
from ingestion.db_connection import Neo4jConnection

logger = get_logger(__name__)


class GraphValidator:
    """Validates graph data integrity"""

    @staticmethod
    def validate_node_counts() -> dict:
        """Validate node counts match expected data"""
        logger.info("Validating node counts...")

        query = """
        CALL apoc.meta.stats() YIELD labels
        RETURN labels
        """

        try:
            results = Neo4jConnection.execute_query(query)
            if results:
                stats = results[0]["labels"]
                logger.info(f"[OK] Node counts: {stats}")
                return stats
        except Exception as e:
            logger.warning(f"Could not retrieve detailed stats: {str(e)}")

        # Fallback: simple count query
        query = """
        MATCH (n)
        RETURN labels(n)[0] as label, count(*) as count
        ORDER BY label
        """

        try:
            results = Neo4jConnection.execute_query(query)
            stats = {}
            for record in results:
                stats[record["label"]] = record["count"]
            logger.info(f"✓ Node counts: {stats}")
            return stats
        except Exception as e:
            logger.error(f"✗ Failed to validate node counts: {str(e)}")
            return {}

    @staticmethod
    def validate_relationships() -> dict:
        """Validate relationship counts"""
        logger.info("Validating relationships...")

        query = """
        MATCH ()-[r]-()
        RETURN type(r) as rel_type, count(*) as count
        ORDER BY rel_type
        """

        try:
            results = Neo4jConnection.execute_query(query)
            stats = {}
            for record in results:
                stats[record["rel_type"]] = record["count"]
            logger.info(f"[OK] Relationship counts: {stats}")
            return stats
        except Exception as e:
            logger.error(f"✗ Failed to validate relationships: {str(e)}")
            return {}

    @staticmethod
    def validate_orphaned_nodes() -> dict:
        """Check for nodes without relationships"""
        logger.info("Checking for orphaned nodes...")

        query = """
        MATCH (n)
        WHERE NOT (n)--()
        RETURN labels(n)[0] as label, count(*) as count
        ORDER BY label
        """

        try:
            results = Neo4jConnection.execute_query(query)
            orphaned = {}
            for record in results:
                orphaned[record["label"]] = record["count"]

            if orphaned:
                logger.warning(f"⚠ Orphaned nodes found: {orphaned}")
            else:
                logger.info("[OK] No orphaned nodes found")

            return orphaned
        except Exception as e:
            logger.error(f"✗ Failed to check orphaned nodes: {str(e)}")
            return {}

    @staticmethod
    def validate_graph_integrity() -> bool:
        """Run comprehensive graph validation"""
        logger.info("=" * 60)
        logger.info("VALIDATING GRAPH INTEGRITY")
        logger.info("=" * 60)

        # Validate nodes
        node_stats = GraphValidator.validate_node_counts()

        # Validate relationships
        rel_stats = GraphValidator.validate_relationships()

        # Check orphaned nodes
        orphaned = GraphValidator.validate_orphaned_nodes()

        logger.info("=" * 60)
        logger.info("[OK] Validation complete")
        logger.info("=" * 60)

        return len(node_stats) > 0 and len(rel_stats) > 0

    @staticmethod
    def get_graph_summary() -> dict:
        """Get comprehensive graph summary"""
        return {
            "nodes": GraphValidator.validate_node_counts(),
            "relationships": GraphValidator.validate_relationships(),
            "orphaned": GraphValidator.validate_orphaned_nodes(),
        }
