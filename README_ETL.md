# Neo4j Graph Database ETL System

This directory contains the complete ETL (Extract-Transform-Load) system for Neo4j graph ingestion.

## Project Structure

```
neo4j_project/
├── config/
│   └── neo4j_config.py          # Central configuration and schema definitions
├── ingestion/
│   ├── db_connection.py         # Neo4j driver and connection management
│   ├── schema_manager.py        # Schema creation, constraints, indexes
│   ├── data_loader.py           # CSV loading and validation
│   ├── node_ingestor.py         # Node ingestion logic
│   ├── relationship_ingestor.py # Relationship ingestion logic
│   └── etl_pipeline.py          # Main ETL orchestrator
├── models/
│   └── graph_model.py           # Data model definitions
├── utils/
│   ├── logger.py                # Logging configuration
│   └── errors.py                # Custom exceptions
├── validation/
│   └── graph_validator.py       # Graph integrity validation
├── queries/
│   ├── analytics.cypher         # Analytics queries
│   ├── visualization.cypher     # Visualization queries
│   └── traversal.cypher         # Graph traversal queries
├── data/                         # CSV data files
├── logs/                         # Execution logs
├── main.py                       # Entry point (simplified testing)
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Neo4j Credentials

Create a local `.env` file or set these environment variables in your shell:

```bash
NEO4J_URI=neo4j+s://your-database-id.databases.neo4j.io
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
```

### 3. Run ETL Pipeline

```bash
python ingestion/etl_pipeline.py
```

This will:
- Initialize Neo4j connection
- Create constraints and indexes
- Ingest all nodes and relationships
- Validate graph integrity
- Generate execution summary

### 4. Query Your Graph

```bash
python queries/example_queries.py
```

## Architecture

### Data Models
- **Nodes**: Company, Investor, Fund, Person, Sector, Location
- **Relationships**: LOCATED_IN, OPERATES_IN, INVESTED_IN, MANAGES, COMMITS_TO, WORKS_AT, WORKS_FOR, BOARD_MEMBER_OF, KNOWS

### Key Features
- ✓ Idempotent ingestion (MERGE operations prevent duplicates)
- ✓ Batch processing for performance
- ✓ Comprehensive error handling and retry logic
- ✓ Transaction management
- ✓ Logging and monitoring
- ✓ Data validation
- ✓ Graph integrity checks
- ✓ Relationship properties (round, amount_usd, strength, etc.)

### Performance Optimizations
- Batch size: 100 records per transaction
- Unique constraints on primary keys
- Indexes on frequently queried properties
- Connection pooling
- Automatic retry on failure

## Configuration

Edit `config/neo4j_config.py` to change:
- Neo4j connection parameters
- Batch size
- Retry attempts
- File paths

## Monitoring

Logs are written to:
- Console: INFO level
- File: `logs/neo4j_etl.log` (DEBUG level)

## Graph Statistics

After ingestion, check statistics:
- Node counts by type
- Relationship counts by type
- Orphaned nodes detection
- Data quality metrics

## Advanced Queries

See `queries/` directory for:
- Network analysis
- Path finding
- Recommendation engines
- Community detection
- Influence mapping

## Troubleshooting

1. **Connection issues**: Check credentials in `config/neo4j_config.py`
2. **File not found**: Ensure CSV files are in `data/` directory
3. **Duplicate errors**: Graph uses MERGE to prevent duplicates
4. **Memory issues**: Reduce BATCH_SIZE in config

## Production Checklist

- [ ] Test with full dataset
- [ ] Monitor ingestion performance
- [ ] Validate data quality
- [ ] Set up automated backups
- [ ] Configure monitoring alerts
- [ ] Document custom queries
- [ ] Performance tune indexes
- [ ] Set up change data capture if needed
