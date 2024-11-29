"""Client for working with Miro API."""

import requests
from typing import Dict, Any, List, Optional
from core.config import settings
from core.security import security_manager

class MiroClient:
    """Client for secure interaction with Miro API."""

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
        """Make a request to Miro API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request data
            
        Returns:
            API response as dictionary
        """
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
        """Get items from the board.
        
        Args:
            item_type: Optional filter by item type
            
        Returns:
            List of board items
        """
        endpoint = f"/boards/{self._board_id}/items"
        params = {"type": item_type} if item_type else {}
        return self._make_request("GET", endpoint, params)["data"]

    def create_card(self, content: str, position: Dict[str, float]) -> Dict[str, Any]:
        """Create a card on the board.
        
        Args:
            content: Card content
            position: Card position (x, y coordinates)
            
        Returns:
            Created card data
        """
        endpoint = f"/boards/{self._board_id}/cards"
        data = {
            "data": {
                "content": content,
                "position": position
            }
        }
        return self._make_request("POST", endpoint, data)

    def update_card(self, card_id: str, content: str) -> Dict[str, Any]:
        """Update a card on the board.
        
        Args:
            card_id: ID of the card to update
            content: New card content
            
        Returns:
            Updated card data
        """
        endpoint = f"/boards/{self._board_id}/cards/{card_id}"
        data = {
            "data": {
                "content": content
            }
        }
        return self._make_request("PATCH", endpoint, data)

    def delete_card(self, card_id: str) -> None:
        """Delete a card from the board.
        
        Args:
            card_id: ID of the card to delete
        """
        endpoint = f"/boards/{self._board_id}/cards/{card_id}"
        self._make_request("DELETE", endpoint)

    def create_connector(self, start_item_id: str, end_item_id: str, 
                        connector_type: str = "straight", style: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a connection between items on the board.
        
        Args:
            start_item_id: ID of the start item
            end_item_id: ID of the end item
            connector_type: Connection type ('straight', 'elbowed', 'curved')
            style: Connection style (color, width, etc.)
            
        Returns:
            Created connector data
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
        """Get list of connectors on the board.
        
        Args:
            item_id: Optional item ID to filter connectors
            
        Returns:
            List of connectors
        """
        endpoint = f"/boards/{self._board_id}/connectors"
        if item_id:
            endpoint += f"?item_id={item_id}"
        return self._make_request("GET", endpoint)["data"]

    def update_connector(self, connector_id: str, 
                        connector_type: Optional[str] = None, 
                        style: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update connector parameters.
        
        Args:
            connector_id: Connector ID
            connector_type: New connector type
            style: New connector style
            
        Returns:
            Updated connector data
        """
        endpoint = f"/boards/{self._board_id}/connectors/{connector_id}"
        data = {"data": {}}
        
        if connector_type:
            data["data"]["shape"] = connector_type
        if style:
            data["data"]["style"] = style
            
        return self._make_request("PATCH", endpoint, data)

    def delete_connector(self, connector_id: str) -> None:
        """Delete a connector from the board.
        
        Args:
            connector_id: ID of the connector to delete
        """
        endpoint = f"/boards/{self._board_id}/connectors/{connector_id}"
        self._make_request("DELETE", endpoint)

    def create_related_cards(self, cards_data: List[Dict[str, Any]], 
                           connection_type: str = "straight") -> List[Dict[str, Any]]:
        """Create multiple connected cards on the board.
        
        Args:
            cards_data: List of card data dictionaries:
                       [{"content": str, "position": Dict[str, float]}, ...]
            connection_type: Type of connection between cards
        
        Returns:
            List of created cards with their connections
        """
        created_cards = []
        previous_card = None

        for card_data in cards_data:
            # Create new card
            new_card = self.create_card(
                content=card_data["content"],
                position=card_data["position"]
            )
            created_cards.append(new_card)

            # If there's a previous card, create connection
            if previous_card:
                self.create_connector(
                    start_item_id=previous_card["id"],
                    end_item_id=new_card["id"],
                    connector_type=connection_type
                )

            previous_card = new_card

        return created_cards

# Create global client instance
miro_client = MiroClient()
