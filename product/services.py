from django.core.cache import cache
from config.settings import CACHE_ENABLED
from product.models import Category


def get_category_from_cache():
    """Получает данные категорий из кэша, если кэш пуст, то поучает данные из базы данных."""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'category_list'
    category = cache.get(key)
    if category is not None:
        return category
    category = Category.objects.all()
    cache.set(key, category)
    return category
