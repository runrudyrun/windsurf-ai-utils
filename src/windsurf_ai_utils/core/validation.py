"""Module for configuration validation."""

import re
from typing import Optional, Dict, Any
import requests
from core.config import settings


def validate_miro_config() -> Dict[str, Any]:
    """Validate Miro configuration.
    
    Returns:
        Dictionary with validation results
        
    Example:
        {
            "valid": True,
            "errors": [],
            "warnings": ["Board ID missing trailing equals sign"]
        }
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Validate access token
    token = settings.miro.access_token.get_secret_value()
    if not token:
        result["valid"] = False
        result["errors"].append("Miro access token is missing")
    elif not re.match(r'^[\w\-_]+$', token):
        result["valid"] = False
        result["errors"].append("Miro access token has invalid format")
        
    # Validate board ID
    board_id = settings.miro.board_id
    if not board_id:
        result["valid"] = False
        result["errors"].append("Miro board ID is missing")
    else:
        # Check if board ID ends with equals sign
        if not board_id.endswith('='):
            result["warnings"].append("Board ID might be missing trailing equals sign")
            
        # Try to clean the board ID
        clean_id = board_id.rstrip('=')
        if not re.match(r'^[\w\-_]+$', clean_id):
            result["valid"] = False
            result["errors"].append("Miro board ID has invalid format")
            
    return result


def validate_clickhouse_config() -> Dict[str, Any]:
    """Validate ClickHouse configuration.
    
    Returns:
        Dictionary with validation results
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Validate host
    if not settings.clickhouse.host:
        result["valid"] = False
        result["errors"].append("ClickHouse host is missing")
        
    # Validate port
    if not isinstance(settings.clickhouse.port, int):
        result["valid"] = False
        result["errors"].append("ClickHouse port must be an integer")
    elif settings.clickhouse.port < 1 or settings.clickhouse.port > 65535:
        result["valid"] = False
        result["errors"].append("ClickHouse port must be between 1 and 65535")
        
    # Validate user
    if not settings.clickhouse.user:
        result["valid"] = False
        result["errors"].append("ClickHouse user is missing")
        
    # Validate password
    if not settings.clickhouse.password.get_secret_value():
        result["valid"] = False
        result["errors"].append("ClickHouse password is missing")
        
    # Validate database
    if not settings.clickhouse.database:
        result["valid"] = False
        result["errors"].append("ClickHouse database is missing")
        
    return result


def validate_all() -> Dict[str, Dict[str, Any]]:
    """Validate all configurations.
    
    Returns:
        Dictionary with validation results for each service
    """
    return {
        "miro": validate_miro_config(),
        "clickhouse": validate_clickhouse_config()
    }
