"""Tests for Miro client."""

import pytest
from unittest.mock import patch, MagicMock
from services.miro.client import MiroClient


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch('services.miro.client.settings') as mock:
        mock.miro.access_token.get_secret_value.return_value = "test_token"
        mock.miro.board_id = "test_board="
        yield mock


@pytest.fixture
def client(mock_settings):
    """Create test client instance."""
    return MiroClient()


def test_create_card_success(client):
    """Test successful card creation."""
    with patch('services.miro.client.requests.request') as mock_request:
        # Setup mock response
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "test_card_id",
            "type": "card"
        }
        mock_request.return_value = mock_response
        
        # Test card creation
        card = client.create_card(
            title="Test Card",
            description="Test Description",
            style={"cardTheme": "#2196f3"},
            position={"x": 0, "y": 0, "origin": "center"}
        )
        
        # Verify request
        mock_request.assert_called_once()
        args = mock_request.call_args
        assert args[1]["method"] == "POST"
        assert "boards/test_board=/cards" in args[1]["url"]
        
        # Verify card data
        assert card["id"] == "test_card_id"
        assert card["type"] == "card"


def test_create_card_error(client):
    """Test card creation error handling."""
    with patch('services.miro.client.requests.request') as mock_request:
        # Setup mock error response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.json.return_value = {
            "type": "error",
            "message": "Test error"
        }
        mock_request.return_value = mock_response
        
        # Test error handling
        with pytest.raises(Exception) as exc:
            client.create_card(
                title="Test Card",
                description="Test Description"
            )
        
        assert "Test error" in str(exc.value)


def test_get_card_url(client):
    """Test card URL generation."""
    url = client.get_card_url("test_card_id")
    assert "test_board=" in url
    assert "test_card_id" in url
