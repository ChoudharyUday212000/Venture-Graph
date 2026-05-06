"""
Neo4j Graph Database - Main Entry Point
Complete graph ingestion system for venture capital ecosystem
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.etl_pipeline import ETLPipeline
from ingestion.db_connection import Neo4jConnection
from validation.graph_validator import GraphValidator
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main entry point - Run complete ETL pipeline"""

    print("\n" + "=" * 80)
    print("NEO4J VENTURE CAPITAL GRAPH DATABASE")
    print("=" * 80)

    # Initialize connection
    try:
        Neo4jConnection.initialize()
        logger.info("✓ Neo4j connection successful\n")
    except Exception as e:
        logger.error(f"✗ Connection failed: {str(e)}")
        return 1

    # Show menu
    print("\nOptions:")
    print("1. Run full ETL pipeline (load all data)")
    print("2. Clear database and reload")
    print("3. View graph statistics")
    print("4. Validate graph integrity")
    print("5. Exit")

    choice = input("\nSelect option (1-5): ").strip()

    if choice == "1":
        pipeline = ETLPipeline()
        success = pipeline.run_full_pipeline(clear_db=False)
        return 0 if success else 1

    elif choice == "2":
        confirm = input("⚠ This will DELETE all data. Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            pipeline = ETLPipeline()
            success = pipeline.run_full_pipeline(clear_db=True)
            return 0 if success else 1
        else:
            logger.info("Operation cancelled")
            return 0

    elif choice == "3":
        stats = GraphValidator.get_graph_summary()
        logger.info("Graph Statistics:")
        logger.info(f"Nodes: {stats['nodes']}")
        logger.info(f"Relationships: {stats['relationships']}")
        logger.info(f"Orphaned: {stats['orphaned']}")
        return 0

    elif choice == "4":
        success = GraphValidator.validate_graph_integrity()
        return 0 if success else 1

    elif choice == "5":
        logger.info("Exiting...")
        Neo4jConnection.close()
        return 0

    else:
        logger.error("Invalid option")
        return 1


if __name__ == "__main__":
    sys.exit(main())