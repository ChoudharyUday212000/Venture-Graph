"""
Relationship ingestion module
Handles loading and creating relationships in Neo4j
"""

import pandas as pd
from typing import Dict, Tuple
from tqdm import tqdm
from utils.logger import get_logger
from ingestion.db_connection import Neo4jConnection
from ingestion.data_loader import DataLoader
from config.neo4j_config import BATCH_SIZE

logger = get_logger(__name__)


class RelationshipIngestor:
    """Ingests relationships into Neo4j"""

    @staticmethod
    def ingest_located_in() -> int:
        """Ingest Company -[LOCATED_IN]-> Location relationships"""
        logger.info("Ingesting LOCATED_IN relationships...")
        df = DataLoader.load_relationship_data("LOCATED_IN")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["company_id", "location_name"])

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="LOCATED_IN"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (c:Company {company_id: row.company_id})
            MATCH (l:Location {location_name: row.location_name})
            MERGE (c)-[:LOCATED_IN]->(l)
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
                logger.error(f"Error ingesting LOCATED_IN batch: {str(e)}")

        logger.info(f"[OK] LOCATED_IN relationships created: {created}")
        return created

    @staticmethod
    def ingest_operates_in() -> int:
        """Ingest Company -[OPERATES_IN]-> Sector relationships"""
        logger.info("Ingesting OPERATES_IN relationships...")
        df = DataLoader.load_relationship_data("OPERATES_IN")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["company_id", "sector_name"])

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="OPERATES_IN"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (c:Company {company_id: row.company_id})
            MATCH (s:Sector {sector_name: row.sector_name})
            MERGE (c)-[:OPERATES_IN]->(s)
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
                logger.error(f"Error ingesting OPERATES_IN batch: {str(e)}")

        logger.info(f"[OK] OPERATES_IN relationships created: {created}")
        return created

    @staticmethod
    def ingest_invested_in() -> int:
        """Ingest Fund -[INVESTED_IN]-> Company relationships with properties"""
        logger.info("Ingesting INVESTED_IN relationships...")
        df = DataLoader.load_relationship_data("INVESTED_IN")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["fund_id", "company_id", "round", "year", "amount_usd"])

        # Convert amount_usd to numeric
        df["amount_usd"] = pd.to_numeric(df["amount_usd"], errors="coerce")
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="INVESTED_IN"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (f:Fund {fund_id: row.fund_id})
            MATCH (c:Company {company_id: row.company_id})
            MERGE (f)-[rel:INVESTED_IN {round: row.round}]->(c)
            SET rel.year = toInteger(row.year),
                rel.amount_usd = toInteger(row.amount_usd)
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
                logger.error(f"Error ingesting INVESTED_IN batch: {str(e)}")

        logger.info(f"[OK] INVESTED_IN relationships created: {created}")
        return created

    @staticmethod
    def ingest_manages() -> int:
        """Ingest Investor -[MANAGES]-> Fund relationships (GPs only)"""
        logger.info("Ingesting MANAGES relationships...")
        df = DataLoader.load_relationship_data("MANAGES")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["investor_id", "fund_id"])

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="MANAGES"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (i:Investor {investor_id: row.investor_id})
            MATCH (f:Fund {fund_id: row.fund_id})
            MERGE (i)-[:MANAGES]->(f)
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
                logger.error(f"Error ingesting MANAGES batch: {str(e)}")

        logger.info(f"[OK] MANAGES relationships created: {created}")
        return created

    @staticmethod
    def ingest_commits_to() -> int:
        """Ingest Investor -[COMMITS_TO]-> Fund relationships (LPs only)"""
        logger.info("Ingesting COMMITS_TO relationships...")
        df = DataLoader.load_relationship_data("COMMITS_TO")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["lp_investor_id", "fund_id", "commitment_usd", "year"])

        # Convert to numeric
        df["commitment_usd"] = pd.to_numeric(df["commitment_usd"], errors="coerce")
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="COMMITS_TO"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (i:Investor {investor_id: row.lp_investor_id})
            MATCH (f:Fund {fund_id: row.fund_id})
            MERGE (i)-[rel:COMMITS_TO]->(f)
            SET rel.commitment_usd = toInteger(row.commitment_usd),
                rel.year = toInteger(row.year)
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
                logger.error(f"Error ingesting COMMITS_TO batch: {str(e)}")

        logger.info(f"[OK] COMMITS_TO relationships created: {created}")
        return created

    @staticmethod
    def ingest_works_at() -> int:
        """Ingest Person -[WORKS_AT]-> Company relationships"""
        logger.info("Ingesting WORKS_AT relationships...")
        df = DataLoader.load_relationship_data("WORKS_AT")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["person_id", "company_id", "title"])

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="WORKS_AT"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (p:Person {person_id: row.person_id})
            MATCH (c:Company {company_id: row.company_id})
            MERGE (p)-[rel:WORKS_AT]->(c)
            SET rel.title = row.title
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
                logger.error(f"Error ingesting WORKS_AT batch: {str(e)}")

        logger.info(f"[OK] WORKS_AT relationships created: {created}")
        return created

    @staticmethod
    def ingest_works_for() -> int:
        """Ingest Person -[WORKS_FOR]-> Investor relationships"""
        logger.info("Ingesting WORKS_FOR relationships...")
        df = DataLoader.load_relationship_data("WORKS_FOR")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["person_id", "investor_id", "title"])

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="WORKS_FOR"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (p:Person {person_id: row.person_id})
            MATCH (i:Investor {investor_id: row.investor_id})
            MERGE (p)-[rel:WORKS_FOR]->(i)
            SET rel.title = row.title
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
                logger.error(f"Error ingesting WORKS_FOR batch: {str(e)}")

        logger.info(f"[OK] WORKS_FOR relationships created: {created}")
        return created

    @staticmethod
    def ingest_board_member_of() -> int:
        """Ingest Person -[BOARD_MEMBER_OF]-> Company relationships"""
        logger.info("Ingesting BOARD_MEMBER_OF relationships...")
        df = DataLoader.load_relationship_data("BOARD_MEMBER_OF")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["person_id", "company_id", "since_year"])

        df["since_year"] = pd.to_numeric(df["since_year"], errors="coerce")

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="BOARD_MEMBER_OF"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (p:Person {person_id: row.person_id})
            MATCH (c:Company {company_id: row.company_id})
            MERGE (p)-[rel:BOARD_MEMBER_OF]->(c)
            SET rel.since_year = toInteger(row.since_year)
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
                logger.error(f"Error ingesting BOARD_MEMBER_OF batch: {str(e)}")

        logger.info(f"[OK] BOARD_MEMBER_OF relationships created: {created}")
        return created

    @staticmethod
    def ingest_knows() -> int:
        """Ingest Person -[KNOWS]-> Person relationships"""
        logger.info("Ingesting KNOWS relationships...")
        df = DataLoader.load_relationship_data("KNOWS")
        df = DataLoader.clean_data(df)

        DataLoader.validate_data(df, ["person1_id", "person2_id", "strength"])

        created = 0

        for i in tqdm(range(0, len(df), BATCH_SIZE), desc="KNOWS"):
            batch = df.iloc[i : i + BATCH_SIZE]

            query = """
            UNWIND $data AS row
            MATCH (p1:Person {person_id: row.person1_id})
            MATCH (p2:Person {person_id: row.person2_id})
            MERGE (p1)-[rel:KNOWS]->(p2)
            SET rel.strength = row.strength
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
                logger.error(f"Error ingesting KNOWS batch: {str(e)}")

        logger.info(f"[OK] KNOWS relationships created: {created}")
        return created

    @staticmethod
    def ingest_all_relationships() -> Dict[str, int]:
        """Ingest all relationship types"""
        results = {}

        results["LOCATED_IN"] = RelationshipIngestor.ingest_located_in()
        results["OPERATES_IN"] = RelationshipIngestor.ingest_operates_in()
        results["INVESTED_IN"] = RelationshipIngestor.ingest_invested_in()
        results["MANAGES"] = RelationshipIngestor.ingest_manages()
        results["COMMITS_TO"] = RelationshipIngestor.ingest_commits_to()
        results["WORKS_AT"] = RelationshipIngestor.ingest_works_at()
        results["WORKS_FOR"] = RelationshipIngestor.ingest_works_for()
        results["BOARD_MEMBER_OF"] = RelationshipIngestor.ingest_board_member_of()
        results["KNOWS"] = RelationshipIngestor.ingest_knows()

        return results
