"""
CSV data loading and processing
Handles reading, validating, and preparing CSV data for ingestion
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Tuple
from utils.logger import get_logger
from utils.errors import DataValidationException
from config.neo4j_config import DATA_DIR, NODE_FILES, RELATIONSHIP_FILES

logger = get_logger(__name__)


class DataLoader:
    """Loads and validates CSV data"""

    @staticmethod
    def load_csv(filename: str) -> pd.DataFrame:
        """Load CSV file and return as DataFrame"""
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        try:
            df = pd.read_csv(filepath)
            logger.debug(f"Loaded {filename}: {len(df)} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            raise DataValidationException(f"Failed to load {filename}: {str(e)}")

    @staticmethod
    def load_node_data(node_label: str) -> pd.DataFrame:
        """Load node CSV data"""
        filename = NODE_FILES.get(node_label)
        if not filename:
            raise ValueError(f"Unknown node type: {node_label}")

        return DataLoader.load_csv(filename)

    @staticmethod
    def load_relationship_data(rel_type: str) -> pd.DataFrame:
        """Load relationship CSV data"""
        filename = RELATIONSHIP_FILES.get(rel_type)
        if not filename:
            raise ValueError(f"Unknown relationship type: {rel_type}")

        return DataLoader.load_csv(filename)

    @staticmethod
    def validate_data(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate that DataFrame has required columns"""
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise DataValidationException(
                f"Missing required columns: {missing}"
            )
        return True

    @staticmethod
    def detect_duplicates(df: pd.DataFrame, key_columns: List[str]) -> Tuple[int, pd.DataFrame]:
        """
        Detect duplicate records based on key columns

        Returns:
            Tuple of (duplicate_count, duplicates_df)
        """
        duplicates = df[df.duplicated(subset=key_columns, keep=False)]
        return len(duplicates), duplicates

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean DataFrame: remove whitespace, handle nulls, standardize formats

        Returns:
            Cleaned DataFrame
        """
        # Strip whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        # Drop completely null rows
        df = df.dropna(how='all')

        logger.debug(f"Cleaned data: {len(df)} rows after cleaning")
        return df

    @staticmethod
    def get_data_summary() -> Dict[str, Dict]:
        """Get summary of all available data"""
        summary = {
            "nodes": {},
            "relationships": {},
        }

        # Node data summary
        for node_label in NODE_FILES.keys():
            try:
                df = DataLoader.load_node_data(node_label)
                summary["nodes"][node_label] = {
                    "count": len(df),
                    "columns": list(df.columns),
                }
            except Exception as e:
                logger.warning(f"Error loading {node_label} data: {str(e)}")

        # Relationship data summary
        for rel_type in RELATIONSHIP_FILES.keys():
            try:
                df = DataLoader.load_relationship_data(rel_type)
                summary["relationships"][rel_type] = {
                    "count": len(df),
                    "columns": list(df.columns),
                }
            except Exception as e:
                logger.warning(f"Error loading {rel_type} data: {str(e)}")

        return summary
