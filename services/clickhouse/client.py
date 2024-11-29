"""Client for working with ClickHouse."""

from typing import List, Dict, Any
from clickhouse_driver import Client
from core.config import settings

class ClickHouseClient:
    """Client for secure interaction with ClickHouse."""

    def __init__(self):
        self._client = Client(
            host=settings.clickhouse.host,
            port=settings.clickhouse.port,
            user=settings.clickhouse.user,
            password=settings.clickhouse.password.get_secret_value(),
            database=settings.clickhouse.database,
        )

    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a query to ClickHouse.
        
        Args:
            query: SQL query string
            params: Query parameters for safe substitution
            
        Returns:
            List of dictionaries with query results
        """
        result = self._client.execute(
            query,
            params or {},
            with_column_types=True
        )
        rows, columns = result
        column_names = [col[0] for col in columns]
        return [dict(zip(column_names, row)) for row in rows]

    def execute_query_stream(self, query: str, params: Dict[str, Any] = None):
        """Stream execution of a query to ClickHouse.
        
        Args:
            query: SQL query string
            params: Query parameters for safe substitution
            
        Yields:
            Individual rows from the query result
        """
        for row in self._client.execute_iter(query, params or {}):
            yield row

    def ping(self) -> bool:
        """Check connection to ClickHouse.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            self._client.execute('SELECT 1')
            return True
        except Exception:
            return False

# Create global client instance
clickhouse_client = ClickHouseClient()
