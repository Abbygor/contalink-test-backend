import hashlib
import logging

from django.core.cache import cache

CACHE_TTL_SECONDS = 5 * 60
CACHE_KEY_PREFIX = "invoices_list"

logger = logging.getLogger(__name__)


def build_cache_key(query_params: dict) -> str:
    sorted_params = sorted(query_params.items())
    raw_key = "&".join(f"{key}={value}" for key, value in sorted_params)
    hashed = hashlib.md5(raw_key.encode()).hexdigest()
    return f"{CACHE_KEY_PREFIX}:{hashed}"


def get_cached_response(cache_key: str):
    try:
        return cache.get(cache_key)
    except Exception:
        logger.warning("cache get failed, falling back to DB")
        return None


def set_cached_response(cache_key: str, response_data: dict) -> None:
    try:
        cache.set(cache_key, response_data, CACHE_TTL_SECONDS)
    except Exception:
        logger.warning("cache set failed")
