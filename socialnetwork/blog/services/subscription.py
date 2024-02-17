from rest_framework.exceptions import APIException
from socialnetwork.users.models import BaseUser
from ..models import Subscription

def subscribe(*, user:BaseUser, email:str) -> Subscription:
    try:
        target = BaseUser.objects.get(email=email)
    except BaseUser.DoesNotExist:
        raise APIException(
            'There is no user with the provided email.'
        )
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    return sub


def unsubscribe(*, user:BaseUser, email:str) -> Subscription:
    try:
        target = BaseUser.objects.get(email=email)
    except BaseUser.DoesNotExist:
        raise APIException(
            'There is no user with the provided email.'
        )
    Subscription.objects.get(subscriber=user, target=target).delete()
