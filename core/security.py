"""Модуль для обеспечения безопасности при работе с чувствительными данными."""

from jose import jwt
from typing import Any, Dict
from .config import settings

class SecurityManager:
    """Менеджер безопасности для работы с чувствительными данными."""
    
    def __init__(self):
        self._encryption_key = settings.security.encryption_key.get_secret_value()

    def encrypt_sensitive_data(self, data: Dict[str, Any]) -> str:
        """Зашифровать чувствительные данные."""
        return jwt.encode(data, self._encryption_key, algorithm='HS256')

    def decrypt_sensitive_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Расшифровать чувствительные данные."""
        return jwt.decode(encrypted_data, self._encryption_key, algorithms=['HS256'])

    @staticmethod
    def mask_sensitive_string(value: str, visible_chars: int = 4) -> str:
        """Замаскировать чувствительную строку, оставив видимыми только последние символы."""
        if not value or len(value) <= visible_chars:
            return '*' * len(value)
        return '*' * (len(value) - visible_chars) + value[-visible_chars:]

# Создаем глобальный экземпляр менеджера безопасности
security_manager = SecurityManager()
