"""Tests for configuration validation."""

import pytest
from unittest.mock import patch, MagicMock
from core.validation import validate_miro_config, validate_clickhouse_config


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch('core.validation.settings') as mock:
        # Mock Miro settings
        mock.miro.access_token.get_secret_value.return_value = "test_token"
        mock.miro.board_id = "test_board="
        
        # Mock ClickHouse settings
        mock.clickhouse.host = "localhost"
        mock.clickhouse.port = 9000
        mock.clickhouse.user = "default"
        mock.clickhouse.password.get_secret_value.return_value = "password"
        mock.clickhouse.database = "default"
        
        yield mock


def test_validate_miro_config_success(mock_settings):
    """Test successful Miro config validation."""
    result = validate_miro_config()
    assert result["valid"]
    assert not result["errors"]
    assert not result["warnings"]


def test_validate_miro_config_missing_token(mock_settings):
    """Test Miro config validation with missing token."""
    mock_settings.miro.access_token.get_secret_value.return_value = ""
    result = validate_miro_config()
    assert not result["valid"]
    assert "token is missing" in result["errors"][0].lower()


def test_validate_miro_config_invalid_board_id(mock_settings):
    """Test Miro config validation with invalid board ID."""
    mock_settings.miro.board_id = "invalid board id"
    result = validate_miro_config()
    assert not result["valid"]
    assert "invalid format" in result["errors"][0].lower()


def test_validate_miro_config_missing_equals(mock_settings):
    """Test Miro config validation with missing equals sign."""
    mock_settings.miro.board_id = "test_board"
    result = validate_miro_config()
    assert result["valid"]  # Still valid
    assert "equals sign" in result["warnings"][0].lower()


def test_validate_clickhouse_config_success(mock_settings):
    """Test successful ClickHouse config validation."""
    result = validate_clickhouse_config()
    assert result["valid"]
    assert not result["errors"]


def test_validate_clickhouse_config_invalid_port(mock_settings):
    """Test ClickHouse config validation with invalid port."""
    mock_settings.clickhouse.port = 70000
    result = validate_clickhouse_config()
    assert not result["valid"]
    assert "port" in result["errors"][0].lower()


def test_validate_clickhouse_config_missing_password(mock_settings):
    """Test ClickHouse config validation with missing password."""
    mock_settings.clickhouse.password.get_secret_value.return_value = ""
    result = validate_clickhouse_config()
    assert not result["valid"]
    assert "password" in result["errors"][0].lower()
