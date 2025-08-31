import logging
from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

def get_all_properties():
    """
    Get all properties from cache if available; otherwise fetch from DB and cache.
    """
    properties = cache.get("all_properties")
    if properties is None:
        # Query the DB and convert to list of dicts for JSON serialization
        properties = list(Property.objects.all().values("id", "title", "description", "price", "location", "created_at"))
        cache.set("all_properties", properties, 3600)  # Cache for 1 hour
    return properties

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache metrics: keyspace hits, misses, and hit ratio.
    """
    redis_conn = get_redis_connection("default")
    info = redis_conn.info("stats")
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests > 0 else 0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }

    logger.error(f"Redis Cache 
