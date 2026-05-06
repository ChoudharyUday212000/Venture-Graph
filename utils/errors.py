"""
Custom exception classes for ETL operations
"""


class Neo4jETLException(Exception):
    """Base exception for Neo4j ETL operations"""
    pass


class ConnectionException(Neo4jETLException):
    """Exception raised when Neo4j connection fails"""
    pass


class SchemaException(Neo4jETLException):
    """Exception raised during schema operations"""
    pass


class DataValidationException(Neo4jETLException):
    """Exception raised during data validation"""
    pass


class IngestDataException(Neo4jETLException):
    """Exception raised during data ingestion"""
    pass


class DuplicateDataException(Neo4jETLException):
    """Exception raised when duplicate data is detected"""
    pass
