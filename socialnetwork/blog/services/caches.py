from django.core.cache import cache

from socialnetwork.users.models import BaseUser
from ..models import (
    Subscription,
    Post
)

def posts_counter(*, user:BaseUser) -> int:
    return Post.objects.filter(author=user).count()

def subscribers_counter(*, user:BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()

def subscriptions_counter(*, user:BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def profile_cache(*, user:BaseUser) -> None:
    profile = {
        'email': user.email,
        'posts_count': posts_counter(user=user),
        'subscribers_count': subscribers_counter(user=user),
        'subscriptions_count': subscriptions_counter(user=user)
    }
    cache.set(key=f'profile_{user.email}', value=profile, timeout=None)
