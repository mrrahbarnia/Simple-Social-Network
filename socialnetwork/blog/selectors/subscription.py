from django.db.models import QuerySet
from rest_framework.exceptions import APIException

from socialnetwork.users.models import BaseUser
from ..models import Subscription

def get_subscribers(*, user:BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.select_related('subscriber').filter(subscriber=user)
    