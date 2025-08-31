from django.core.cache import cache
from .models import Property

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

