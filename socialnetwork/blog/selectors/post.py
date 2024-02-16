from django.db.models import QuerySet

from socialnetwork.users.models import BaseUser
from ..filters import PostFilter
from ..models import (
    Post,
    Subscription
)

def post_list(*, filters=None, user:BaseUser, self_include:bool = True) -> QuerySet[Post]:
    filters = filters or {}
    subscription = list(
        Subscription.objects.filter(subscriber=user).values_list('target', flat=True)
    )

    if self_include:
        subscription.append(user.id)

    if subscription:
        queryset = Post.objects.filter(author__in=subscription)
        return PostFilter(filters, queryset).qs

    return Post.objects.none()

