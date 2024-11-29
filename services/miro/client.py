"""Клиент для работы с Miro API."""

import requests
from typing import Dict, Any, List, Optional
from core.config import settings
from core.security import security_manager

class MiroClient:
    """Клиент для безопасной работы с Miro API."""

    def __init__(self):
        self._base_url = "https://api.miro.com/v2"
        self._token = settings.miro.access_token.get_secret_value()
        self._board_id = settings.miro.board_id
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}"
        }

    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполнить запрос к Miro API."""
        url = f"{self._base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self._headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def get_board_items(self, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Получить элементы с доски."""
        endpoint = f"/boards/{self._board_id}/items"
        params = {"type": item_type} if item_type else {}
        return self._make_request("GET", endpoint, params)["data"]

    def create_card(self, content: str, position: Dict[str, float]) -> Dict[str, Any]:
        """Создать карточку на доске."""
        endpoint = f"/boards/{self._board_id}/cards"
        data = {
            "data": {
                "content": content,
                "position": position
            }
        }
        return self._make_request("POST", endpoint, data)

    def update_card(self, card_id: str, content: str) -> Dict[str, Any]:
        """Обновить карточку на доске."""
        endpoint = f"/boards/{self._board_id}/cards/{card_id}"
        data = {
            "data": {
                "content": content
            }
        }
        return self._make_request("PATCH", endpoint, data)

    def delete_card(self, card_id: str) -> None:
        """Удалить карточку с доски."""
        endpoint = f"/boards/{self._board_id}/cards/{card_id}"
        self._make_request("DELETE", endpoint)

    def create_connector(self, start_item_id: str, end_item_id: str, 
                        connector_type: str = "straight", style: Dict[str, Any] = None) -> Dict[str, Any]:
        """Создать связь между элементами на доске.
        
        Args:
            start_item_id: ID начального элемента
            end_item_id: ID конечного элемента
            connector_type: Тип связи ('straight', 'elbowed', 'curved')
            style: Стиль связи (цвет, толщина и т.д.)
        """
        endpoint = f"/boards/{self._board_id}/connectors"
        
        if style is None:
            style = {
                "strokeColor": "#000000",
                "strokeWidth": 1,
                "strokeStyle": "normal"
            }

        data = {
            "data": {
                "startItem": {
                    "id": start_item_id
                },
                "endItem": {
                    "id": end_item_id
                },
                "shape": connector_type,
                "style": style
            }
        }
        
        return self._make_request("POST", endpoint, data)

    def get_connectors(self, item_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Получить список связей на доске.
        
        Args:
            item_id: Опциональный ID элемента для фильтрации связей
        """
        endpoint = f"/boards/{self._board_id}/connectors"
        if item_id:
            endpoint += f"?item_id={item_id}"
        return self._make_request("GET", endpoint)["data"]

    def update_connector(self, connector_id: str, 
                        connector_type: Optional[str] = None, 
                        style: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Обновить параметры связи.
        
        Args:
            connector_id: ID связи
            connector_type: Новый тип связи
            style: Новый стиль связи
        """
        endpoint = f"/boards/{self._board_id}/connectors/{connector_id}"
        data = {"data": {}}
        
        if connector_type:
            data["data"]["shape"] = connector_type
        if style:
            data["data"]["style"] = style
            
        return self._make_request("PATCH", endpoint, data)

    def delete_connector(self, connector_id: str) -> None:
        """Удалить связь с доски.
        
        Args:
            connector_id: ID связи для удаления
        """
        endpoint = f"/boards/{self._board_id}/connectors/{connector_id}"
        self._make_request("DELETE", endpoint)

    def create_related_cards(self, cards_data: List[Dict[str, Any]], 
                           connection_type: str = "straight") -> List[Dict[str, Any]]:
        """Создать несколько связанных карточек на доске.
        
        Args:
            cards_data: Список словарей с данными карточек:
                       [{"content": str, "position": Dict[str, float]}, ...]
            connection_type: Тип связи между карточками
        
        Returns:
            Список созданных карточек с их связями
        """
        created_cards = []
        previous_card = None

        for card_data in cards_data:
            # Создаем новую карточку
            new_card = self.create_card(
                content=card_data["content"],
                position=card_data["position"]
            )
            created_cards.append(new_card)

            # Если есть предыдущая карточка, создаем связь
            if previous_card:
                self.create_connector(
                    start_item_id=previous_card["id"],
                    end_item_id=new_card["id"],
                    connector_type=connection_type
                )

            previous_card = new_card

        return created_cards

# Создаем глобальный экземпляр клиента
miro_client = MiroClient()
