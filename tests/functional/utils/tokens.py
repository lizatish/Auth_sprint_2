from redis import Redis


def get_revoked_access_tokens(user_id: str, redis: Redis) -> list[str]:
    """Возвращает отозванные access-token-ы"""
    revoked_keys = redis.keys(f"access_{user_id}*")
    revoked_values = []
    for key in revoked_keys:
        val = redis.get(key)
        revoked_values.append(val)
    return revoked_values
