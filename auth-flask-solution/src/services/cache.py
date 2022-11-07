import datetime

from flask import current_app

from db.redis import CacheStorage


class CacheService:
    """Сервис кеширования."""

    def __init__(self, storage: CacheStorage):
        """Инициализация сервиса."""
        self.db = storage

    def set_revoked_access_token(self, user_id: str, revoked_access_token: str):
        """Устанавливает отозванный access-token"""
        self.db.set(
            f"access_{user_id}_{datetime.datetime.utcnow()}",
            revoked_access_token,
            current_app.config['CACHE_REVOKED_ACCESS_TOKEN_EXPIRED_SEC'],
        )

    def set_refresh_token(self, user_id: str, refresh_token: str):
        """Устанавливает актуальный refresh-token"""
        self.db.set(
            f"refresh_{user_id}",
            refresh_token,
            current_app.config['CACHE_REFRESH_TOKEN_EXPIRED_SEC'],
        )

    def get_revoked_access_token(self, user_id: str) -> list[str]:
        """Возвращает отозванный access-token"""
        revoked_keys = self.db.keys(f"access_{user_id}*")
        revoked_values = []
        for key in revoked_keys:
            val = self.db.get(key)
            revoked_values.append(val)
        return revoked_values

    def get_refresh_token(self, user_id: str) -> str:
        """Возвращает актуальный refresh-token"""
        return self.db.get(f"refresh_{user_id}")

    def delete_refresh_token(self, user_id: str) -> str:
        """Возвращает актуальный refresh-token"""
        return self.db.delete(f"refresh_{user_id}")
