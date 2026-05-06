"""
Logging utility module for ETL operations
"""

import logging
import logging.config
import os
from config.neo4j_config import LOGGING_CONFIG, LOG_DIR

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(name)
