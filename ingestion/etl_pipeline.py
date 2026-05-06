"""
Neo4j ETL Pipeline - Main Orchestrator
Coordinates the complete data ingestion process
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import get_logger
from ingestion.db_connection import Neo4jConnection
from ingestion.schema_manager import SchemaManager
from ingestion.node_ingestor import NodeIngestor
from ingestion.relationship_ingestor import RelationshipIngestor
from validation.graph_validator import GraphValidator

logger = get_logger(__name__)


class ETLPipeline:
    """Orchestrates the complete ETL pipeline"""

    def __init__(self):
        self.start_time = None
        self.stats = {
            "nodes": {},
            "relationships": {},
        }

    def run_full_pipeline(self, clear_db: bool = False) -> bool:
        """
        Run complete ETL pipeline

        Args:
            clear_db: If True, clears database before ingestion (use with caution!)

        Returns:
            True if successful, False otherwise
        """
        try:
            self.start_time = time.time()

            logger.info("\n" + "=" * 80)
            logger.info("STARTING NEO4J ETL PIPELINE")
            logger.info("=" * 80 + "\n")

            # Step 1: Initialize connection
            logger.info("STEP 1: Initializing Neo4j connection...")
            driver = Neo4jConnection.initialize()
            logger.info("✓ Connection established\n")

            # Step 2: Setup schema
            logger.info("STEP 2: Setting up graph schema...")
            SchemaManager.setup_schema()
            logger.info("")

            # Step 3: Clear database if requested
            if clear_db:
                logger.warning(
                    "STEP 3: Clearing database (as requested)..."
                )
                SchemaManager.clear_database(confirm=True)
                logger.info("")

            # Step 4: Ingest nodes
            logger.info("STEP 4: Ingesting nodes...")
            node_results = NodeIngestor.ingest_all_nodes()
            self.stats["nodes"] = node_results
            logger.info("")

            # Step 5: Ingest relationships
            logger.info("STEP 5: Ingesting relationships...")
            rel_results = RelationshipIngestor.ingest_all_relationships()
            self.stats["relationships"] = rel_results
            logger.info("")

            # Step 6: Validate graph
            logger.info("STEP 6: Validating graph integrity...")
            validation_result = GraphValidator.validate_graph_integrity()
            logger.info("")

            # Step 7: Summary
            self._print_summary()

            logger.info("\n" + "=" * 80)
            logger.info("[OK] ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80 + "\n")

            return validation_result

        except Exception as e:
            logger.error(f"\n✗ ETL PIPELINE FAILED: {str(e)}\n")
            return False

        finally:
            # Close connection
            Neo4jConnection.close()

    def _print_summary(self) -> None:
        """Print ETL execution summary"""
        elapsed_time = time.time() - self.start_time

        logger.info("=" * 80)
        logger.info("ETL EXECUTION SUMMARY")
        logger.info("=" * 80)

        # Node summary
        logger.info("\nNODES INGESTED:")
        total_nodes = 0
        for node_type, (created, updated) in self.stats["nodes"].items():
            total = created + updated
            total_nodes += total
            logger.info(f"  {node_type}: {total} (created: {created}, updated: {updated})")

        # Relationship summary
        logger.info("\nRELATIONSHIPS CREATED:")
        total_rels = 0
        for rel_type, count in self.stats["relationships"].items():
            total_rels += count
            logger.info(f"  {rel_type}: {count}")

        logger.info(f"\nTOTAL NODES: {total_nodes}")
        logger.info(f"TOTAL RELATIONSHIPS: {total_rels}")
        logger.info(f"EXECUTION TIME: {elapsed_time:.2f} seconds")

        logger.info("\n" + "=" * 80)


def main():
    """Main entry point"""
    pipeline = ETLPipeline()

    # Run pipeline without clearing database by default
    # Set clear_db=True to clear before ingestion
    success = pipeline.run_full_pipeline(clear_db=False)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
