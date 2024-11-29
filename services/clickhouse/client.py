"""Клиент для работы с ClickHouse."""

from typing import List, Dict, Any
from clickhouse_driver import Client
from core.config import settings

class ClickHouseClient:
    """Клиент для безопасной работы с ClickHouse."""

    def __init__(self):
        self._client = Client(
            host=settings.clickhouse.host,
            port=settings.clickhouse.port,
            user=settings.clickhouse.user,
            password=settings.clickhouse.password.get_secret_value(),
            database=settings.clickhouse.database,
        )

    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Выполнить запрос к ClickHouse."""
        result = self._client.execute(
            query,
            params or {},
            with_column_types=True
        )
        rows, columns = result
        column_names = [col[0] for col in columns]
        return [dict(zip(column_names, row)) for row in rows]

    def execute_query_stream(self, query: str, params: Dict[str, Any] = None):
        """Потоковое выполнение запроса к ClickHouse."""
        for row in self._client.execute_iter(query, params or {}):
            yield row

    def ping(self) -> bool:
        """Проверить подключение к ClickHouse."""
        try:
            self._client.execute('SELECT 1')
            return True
        except Exception:
            return False

# Создаем глобальный экземпляр клиента
clickhouse_client = ClickHouseClient()
