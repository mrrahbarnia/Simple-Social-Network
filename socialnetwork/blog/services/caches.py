from django.core.cache import cache

from socialnetwork.users.models import BaseUser
from socialnetwork.users.models import Profile
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

def update_cache_profiles():
    profiles = cache.keys('profile_*')

    for profile_key in profiles: # profile_mohammadreza@gmail.com
        email = profile_key.replace('profile_', '')
        cached_data = cache.get(profile_key)
        try:
            profile = Profile.objects.get(user__email=email)
            profile.posts_count = cached_data.get('posts_count')
            profile.subscribers_count = cached_data.get('subscribers_count')
            profile.subscriptions_count = cached_data.get('subscriptions_count')
            profile.save()
        except Exception as ex:
            print(ex)
