"""Client for working with Miro API."""

import requests
import json
from typing import Dict, Any, List, Optional
from core.config import settings
from core.security import security_manager

class MiroClient:
    """Client for secure interaction with Miro API."""

    def __init__(self):
        """Initialize Miro client."""
        self._base_url = "https://api.miro.com/v2"
        self._token = settings.miro.access_token.get_secret_value()
        self._board_id = settings.miro.board_id  # Using full board ID including equals sign
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}"
        }

    def _make_request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make request to Miro API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            
        Returns:
            Response data
            
        Raises:
            Exception: If request fails
        """
        url = f"{self._base_url}/{endpoint}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        
        # Log request details for debugging
        print(f"\nMaking request to: {url}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        if data:
            print(f"Data: {json.dumps(data, indent=2)}")
            
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data
        )
        
        if not response.ok:
            print(f"Error response: {json.dumps(response.json(), indent=2)}")
            response.raise_for_status()
            
        return response.json()
        
    def get_current_user(self) -> Dict[str, Any]:
        """Get information about the current user.
        
        Returns:
            Current user data
        """
        return self._make_request("GET", "boards")  # Using boards endpoint to check token

    def get_boards(self, team_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of available boards.
        
        Args:
            team_id: Optional team ID to filter boards
            
        Returns:
            List of boards
        """
        endpoint = "boards"
        if team_id:
            endpoint += f"?team_id={team_id}"
        return self._make_request("GET", endpoint)

    def get_board_info(self) -> Dict[str, Any]:
        """Get information about the current board.
        
        Returns:
            Board data
        """
        return self._make_request("GET", f"boards/{self._board_id}")

    def get_board_items(self, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get items from the board.
        
        Args:
            item_type: Optional filter by item type
            
        Returns:
            List of board items
        """
        endpoint = f"boards/{self._board_id}/items"
        if item_type:
            endpoint += f"?type={item_type}"
        return self._make_request("GET", endpoint)

    def create_card(self, title: str, description: str, style: Dict[str, Any] = None, position: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a card on the board.
        
        Args:
            title: Card title
            description: Card description
            style: Optional card style (e.g. {"fillColor": "#2196f3"})
            position: Optional card position (e.g. {"x": 0, "y": 0, "origin": "center"})
            
        Returns:
            Created card data
        """
        endpoint = f"boards/{self._board_id}/cards"  # Using /cards endpoint
        
        data = {
            "data": {
                "title": title,
                "description": description
            }
        }
        
        if style:
            data["style"] = style
            
        if position:
            data["position"] = position
            
        return self._make_request("POST", endpoint, data=data)

    def update_card(self, card_id: str, title: str = None, description: str = None, style: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update a card on the board.
        
        Args:
            card_id: ID of the card to update
            title: Optional new title
            description: Optional new description
            style: Optional new style (e.g. {"cardTheme": "#2196f3"})
            
        Returns:
            Updated card data
        """
        endpoint = f"boards/{self._board_id}/cards/{card_id}"
        
        data = {"data": {}}
        if title is not None:
            data["data"]["title"] = title
        if description is not None:
            data["data"]["description"] = description
        if style is not None:
            data["style"] = style
            
        return self._make_request("PATCH", endpoint, data=data)

    def delete_card(self, card_id: str) -> None:
        """Delete a card from the board.
        
        Args:
            card_id: ID of the card to delete
        """
        endpoint = f"boards/{self._board_id}/cards/{card_id}"
        self._make_request("DELETE", endpoint)

    def get_card_url(self, card_id: str) -> str:
        """Get URL to view the card on Miro board.
        
        Args:
            card_id: ID of the card
            
        Returns:
            URL to view the card
        """
        return f"https://miro.com/app/board/{self._board_id}/?moveToWidget={card_id}"

    def check_token(self) -> bool:
        """Check if the token is valid.
        
        Returns:
            True if the token is valid, False otherwise
        """
        try:
            self.get_current_user()
            return True
        except requests.exceptions.HTTPError:
            return False

    def check_board(self) -> bool:
        """Check if the board exists.
        
        Returns:
            True if the board exists, False otherwise
        """
        try:
            self.get_board_info()
            return True
        except requests.exceptions.HTTPError:
            return False

# Create global client instance
miro_client = MiroClient()
