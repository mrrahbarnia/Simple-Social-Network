from celery import shared_task

from .services.caches import update_cache_profiles

@shared_task
def update_profiles():
    update_cache_profiles()