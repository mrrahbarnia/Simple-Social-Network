from django.db.models import QuerySet

from socialnetwork.users.models import BaseUser
from ..filters import PostFilter
from ..models import (
    Post,
    Subscription
)

def post_list(*, filters=None, user:BaseUser, self_include:bool = True) -> QuerySet[Post]:
    filters = filters or {}
    subscriptions = list(
        Subscription.objects.filter(subscriber=user).values_list('target', flat=True)
    )

    if self_include:
        subscriptions.append(user.id)

    if subscriptions:
        queryset = Post.objects.select_related('author').filter(author__in=subscriptions)
        return PostFilter(filters, queryset).qs

    return Post.objects.none()

def post_detail(*, slug:str, user:BaseUser, self_include:bool = True) -> Post:
    subscriptions = list(Subscription.objects.filter(
        subscriber=user).values_list('target', flat=True)
    )
    if self_include:
        subscriptions.append(user.id)

    if subscriptions:
        return Post.objects.get(slug=slug, author__in=subscriptions)

    return Post.objects.none()
