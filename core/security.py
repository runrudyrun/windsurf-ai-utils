"""Module for ensuring security when working with sensitive data."""

from jose import jwt
from typing import Any, Dict
from .config import settings

class SecurityManager:
    """Security manager for handling sensitive data."""
    
    def __init__(self):
        self._encryption_key = settings.security.encryption_key.get_secret_value()

    def encrypt_sensitive_data(self, data: Dict[str, Any]) -> str:
        """Encrypt sensitive data."""
        return jwt.encode(data, self._encryption_key, algorithm='HS256')

    def decrypt_sensitive_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt sensitive data."""
        return jwt.decode(encrypted_data, self._encryption_key, algorithms=['HS256'])

    @staticmethod
    def mask_sensitive_string(value: str, visible_chars: int = 4) -> str:
        """Mask sensitive string, leaving only the last few characters visible.
        
        Args:
            value: String to mask
            visible_chars: Number of characters to leave visible at the end
        """
        if not value or len(value) <= visible_chars:
            return '*' * len(value)
        return '*' * (len(value) - visible_chars) + value[-visible_chars:]

# Create global security manager instance
security_manager = SecurityManager()
