from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Caches the full view for 15 minutes
def property_list(request):
    data = get_all_properties()  # Use low-level cache
    return JsonResponse({"data": data})
