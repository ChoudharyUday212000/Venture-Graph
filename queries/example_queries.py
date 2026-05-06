"""
Example queries for Neo4j graph
Demonstrates how to query the loaded graph data
"""

from ingestion.db_connection import Neo4jConnection
from utils.logger import get_logger

logger = get_logger(__name__)


class ExampleQueries:
    """Collection of example graph queries"""

    @staticmethod
    def example_1_all_companies():
        """Example 1: Get all companies"""
        query = "MATCH (c:Company) RETURN c.name, c.sector, c.stage LIMIT 10"
        results = Neo4jConnection.execute_query(query)
        print("\n📊 All Companies:")
        for record in results:
            print(f"  - {record['c.name']} ({record['c.sector']}, {record['c.stage']})")
        return results

    @staticmethod
    def example_2_investor_portfolio():
        """Example 2: Show portfolio of specific investor"""
        query = """
        MATCH (i:Investor {investor_id: 'I1'})-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)
        RETURN i.name as investor, f.name as fund, c.name as company, 
               c.stage as stage, c.sector as sector
        """
        results = Neo4jConnection.execute_query(query)
        print("\n💼 Investor I1 Portfolio:")
        for record in results:
            print(
                f"  Fund: {record['fund']}, Company: {record['company']} "
                f"({record['stage']}, {record['sector']})"
            )
        return results

    @staticmethod
    def example_3_top_investors():
        """Example 3: Find most active investors"""
        query = """
        MATCH (i:Investor)-[:MANAGES]-(f:Fund)-[:INVESTED_IN]->(c:Company)
        RETURN i.name as investor, count(distinct c) as portfolio_size
        ORDER BY portfolio_size DESC
        """
        results = Neo4jConnection.execute_query(query)
        print("\n👥 Top Investors by Portfolio Size:")
        for record in results:
            print(f"  - {record['investor']}: {record['portfolio_size']} companies")
        return results

    @staticmethod
    def example_4_capital_by_sector():
        """Example 4: Total capital deployed by sector"""
        query = """
        MATCH (f:Fund)-[inv:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
        RETURN s.sector_name as sector, sum(inv.amount_usd) as total_usd
        ORDER BY total_usd DESC
        """
        results = Neo4jConnection.execute_query(query)
        print("\n💰 Capital Deployed by Sector:")
        for record in results:
            print(f"  - {record['sector']}: ${record['total_usd']:,}")
        return results

    @staticmethod
    def example_5_investment_network():
        """Example 5: Find co-investment relationships"""
        query = """
        MATCH (i1:Investor)-[:MANAGES]-(f:Fund)-[:INVESTED_IN]->(c:Company)<-[:INVESTED_IN]-(f2:Fund)-[:MANAGES]-(i2:Investor)
        WHERE i1.investor_id < i2.investor_id
        RETURN i1.name as investor1, i2.name as investor2, 
               count(distinct c) as shared_investments, collect(distinct c.name) as companies
        ORDER BY shared_investments DESC
        LIMIT 5
        """
        results = Neo4jConnection.execute_query(query)
        print("\n🤝 Co-Investment Relationships:")
        for record in results:
            print(
                f"  - {record['investor1']} & {record['investor2']}: "
                f"{record['shared_investments']} co-investments"
            )
        return results

    @staticmethod
    def example_6_company_funding_journey():
        """Example 6: Track company funding progression"""
        query = """
        MATCH (c:Company {company_id: 'C2'})<-[inv:INVESTED_IN]-(f:Fund)
        RETURN c.name, f.name, inv.round, inv.year, inv.amount_usd
        ORDER BY inv.year
        """
        results = Neo4jConnection.execute_query(query)
        print("\n📈 Company C2 Funding Journey:")
        for record in results:
            print(
                f"  Year {record['inv.year']}: {record['inv.round']} "
                f"(${record['inv.amount_usd']:,}) from {record['f.name']}"
            )
        return results

    @staticmethod
    def example_7_geographic_presence():
        """Example 7: Investment presence by location"""
        query = """
        MATCH (l:Location)<-[:LOCATED_IN]-(c:Company)
        OPTIONAL MATCH (c)<-[inv:INVESTED_IN]-(f:Fund)
        RETURN l.location_name as location, count(distinct c) as companies,
               count(distinct inv) as investments, sum(inv.amount_usd) as total_usd
        ORDER BY total_usd DESC
        """
        results = Neo4jConnection.execute_query(query)
        print("\n🌍 Geographic Investment Distribution:")
        for record in results:
            print(
                f"  - {record['location']}: {record['companies']} companies, "
                f"${record['total_usd']:,} invested"
            )
        return results

    @staticmethod
    def example_8_lp_commitments():
        """Example 8: LP fund commitments"""
        query = """
        MATCH (lp:Investor {investor_type: 'LP'})-[commit:COMMITS_TO]->(f:Fund)
        RETURN lp.name as lp, f.name as fund, commit.commitment_usd as committed
        ORDER BY committed DESC
        """
        results = Neo4jConnection.execute_query(query)
        print("\n💸 LP Commitments:")
        for record in results:
            print(f"  - {record['lp']} committed ${record['committed']:,} to {record['fund']}")
        return results

    @staticmethod
    def example_9_network_connections():
        """Example 9: Strong personal connections"""
        query = """
        MATCH (p1:Person)-[k:KNOWS]->(p2:Person)
        WHERE k.strength = 'strong'
        OPTIONAL MATCH (p1)-[:WORKS_AT|WORKS_FOR]->(org1)
        OPTIONAL MATCH (p2)-[:WORKS_AT|WORKS_FOR]->(org2)
        RETURN p1.name as person1, p2.name as person2, k.strength as strength
        LIMIT 10
        """
        results = Neo4jConnection.execute_query(query)
        print("\n🔗 Strong Personal Connections:")
        for record in results:
            print(f"  - {record['person1']} <-> {record['person2']} ({record['strength']})")
        return results

    @staticmethod
    def example_10_sector_specialists():
        """Example 10: Investors specializing in sectors"""
        query = """
        MATCH (i:Investor)-[:MANAGES]->(f:Fund)-[:INVESTED_IN]->(c:Company)-[:OPERATES_IN]->(s:Sector)
        WITH i, s, count(distinct c) as sector_investments
        WHERE sector_investments >= 2
        RETURN i.name as investor, s.sector_name as sector, sector_investments
        ORDER BY i.name, sector_investments DESC
        """
        results = Neo4jConnection.execute_query(query)
        print("\n🎯 Investor Sector Specialization:")
        for record in results:
            print(
                f"  - {record['investor']} in {record['sector']}: "
                f"{record['sector_investments']} investments"
            )
        return results


def run_all_examples():
    """Run all example queries"""
    try:
        Neo4jConnection.initialize()

        print("\n" + "=" * 80)
        print("RUNNING NEO4J GRAPH QUERY EXAMPLES")
        print("=" * 80)

        ExampleQueries.example_1_all_companies()
        ExampleQueries.example_2_investor_portfolio()
        ExampleQueries.example_3_top_investors()
        ExampleQueries.example_4_capital_by_sector()
        ExampleQueries.example_5_investment_network()
        ExampleQueries.example_6_company_funding_journey()
        ExampleQueries.example_7_geographic_presence()
        ExampleQueries.example_8_lp_commitments()
        ExampleQueries.example_9_network_connections()
        ExampleQueries.example_10_sector_specialists()

        print("\n" + "=" * 80)
        print("✓ Examples completed")
        print("=" * 80 + "\n")

    except Exception as e:
        logger.error(f"Error running examples: {str(e)}")
    finally:
        Neo4jConnection.close()


if __name__ == "__main__":
    run_all_examples()
