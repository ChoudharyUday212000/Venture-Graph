"""
Node ingestion module
Handles loading and creating nodes in Neo4j
"""

import pandas as pd
from typing import Dict, List, Tuple
from tqdm import tqdm
from utils.logger import get_logger
from ingestion.db_connection import Neo4jConnection
from ingestion.data_loader import DataLoader
from config.neo4j_config import BATCH_SIZE

logger = get_logger(__name__)


class NodeIngestor:
    """Ingests nodes into Neo4j"""

    @staticmethod
    def ingest_companies() -> Tuple[int, int]:
        """Ingest Company nodes"""
        logger.info("Ingesting Company nodes...")
        df = DataLoader.load_node_data("Company")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["company_id", "name", "sector", "stage", "country"])

        created, updated = 0, 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Companies"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MERGE (c:Company {company_id: row.company_id})
            SET c.name = row.name,
                c.sector = row.sector,
                c.stage = row.stage,
                c.country = row.country
            RETURN count(*) as total
            """

            try:
                result = Neo4jConnection.execute_query(
                    query,
                    {"data": batch.to_dict("records")},
                    write_access=True,
                )
                created += result[0]["total"] if result else 0
            except Exception as e:
                logger.error(f"Error ingesting company batch: {str(e)}")

        logger.info(f"[OK] Companies ingested: {created}")
        return created, updated

    @staticmethod
    def ingest_investors() -> Tuple[int, int]:
        """Ingest Investor nodes"""
        logger.info("Ingesting Investor nodes...")
        df = DataLoader.load_node_data("Investor")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(
            df, ["investor_id", "name", "investor_type", "hq_country"]
        )

        created, updated = 0, 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Investors"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MERGE (i:Investor {investor_id: row.investor_id})
            SET i.name = row.name,
                i.investor_type = row.investor_type,
                i.hq_country = row.hq_country
            RETURN count(*) as total
            """

            try:
                result = Neo4jConnection.execute_query(
                    query,
                    {"data": batch.to_dict("records")},
                    write_access=True,
                )
                created += result[0]["total"] if result else 0
            except Exception as e:
                logger.error(f"Error ingesting investor batch: {str(e)}")

        logger.info(f"[OK] Investors ingested: {created}")
        return created, updated

    @staticmethod
    def ingest_funds() -> Tuple[int, int]:
        """Ingest Fund nodes"""
        logger.info("Ingesting Fund nodes...")
        df = DataLoader.load_node_data("Fund")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["fund_id", "name", "vintage", "strategy"])

        created, updated = 0, 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Funds"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MERGE (f:Fund {fund_id: row.fund_id})
            SET f.name = row.name,
                f.vintage = row.vintage,
                f.strategy = row.strategy
            RETURN count(*) as total
            """

            try:
                result = Neo4jConnection.execute_query(
                    query,
                    {"data": batch.to_dict("records")},
                    write_access=True,
                )
                created += result[0]["total"] if result else 0
            except Exception as e:
                logger.error(f"Error ingesting fund batch: {str(e)}")

        logger.info(f"[OK] Funds ingested: {created}")
        return created, updated

    @staticmethod
    def ingest_people() -> Tuple[int, int]:
        """Ingest Person nodes"""
        logger.info("Ingesting Person nodes...")
        df = DataLoader.load_node_data("Person")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["person_id", "name", "role"])

        created, updated = 0, 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="People"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MERGE (p:Person {person_id: row.person_id})
            SET p.name = row.name,
                p.role = row.role
            RETURN count(*) as total
            """

            try:
                result = Neo4jConnection.execute_query(
                    query,
                    {"data": batch.to_dict("records")},
                    write_access=True,
                )
                created += result[0]["total"] if result else 0
            except Exception as e:
                logger.error(f"Error ingesting person batch: {str(e)}")

        logger.info(f"[OK] People ingested: {created}")
        return created, updated

    @staticmethod
    def ingest_sectors() -> Tuple[int, int]:
        """Ingest Sector nodes"""
        logger.info("Ingesting Sector nodes...")
        df = DataLoader.load_node_data("Sector")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["sector_name"])

        created, updated = 0, 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Sectors"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MERGE (s:Sector {sector_name: row.sector_name})
            RETURN count(*) as total
            """

            try:
                result = Neo4jConnection.execute_query(
                    query,
                    {"data": batch.to_dict("records")},
                    write_access=True,
                )
                created += result[0]["total"] if result else 0
            except Exception as e:
                logger.error(f"Error ingesting sector batch: {str(e)}")

        logger.info(f"[OK] Sectors ingested: {created}")
        return created, updated

    @staticmethod
    def ingest_locations() -> Tuple[int, int]:
        """Ingest Location nodes"""
        logger.info("Ingesting Location nodes...")
        df = DataLoader.load_node_data("Location")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["location_name"])

        created, updated = 0, 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Locations"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MERGE (l:Location {location_name: row.location_name})
            RETURN count(*) as total
            """

            try:
                result = Neo4jConnection.execute_query(
                    query,
                    {"data": batch.to_dict("records")},
                    write_access=True,
                )
                created += result[0]["total"] if result else 0
            except Exception as e:
                logger.error(f"Error ingesting location batch: {str(e)}")

        logger.info(f"[OK] Locations ingested: {created}")
        return created, updated

    @staticmethod
    def ingest_all_nodes() -> Dict[str, Tuple[int, int]]:
        """Ingest all node types"""
        results = {}

        results["Company"] = NodeIngestor.ingest_companies()
        results["Investor"] = NodeIngestor.ingest_investors()
        results["Fund"] = NodeIngestor.ingest_funds()
        results["Person"] = NodeIngestor.ingest_people()
        results["Sector"] = NodeIngestor.ingest_sectors()
        results["Location"] = NodeIngestor.ingest_locations()

        return results
