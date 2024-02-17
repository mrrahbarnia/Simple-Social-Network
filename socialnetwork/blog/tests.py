import pytest

from socialnetwork.users.models import BaseUser
from .services.post import create_post
from .services.subscription import (
    subscribe,
    unsubscribe
)
from .selectors.subscription import (
    get_subscribers
)
from .models import (
    Post,
    Subscription
)


class TestBlogBusinessLogic:

    @pytest.mark.django_db
    def test_post_business_logics(self):
        user1 = BaseUser.objects.create_user(
            email='user1@example.com',
            password='1234@example.com'
        )

        post1 = create_post(
            user=user1,
            title='Sample title',
            content='Sample content'
        )

        post2 = create_post(
            user=user1,
            title='Sample title1',
            content='Sample content1'
        )

        assert Post.objects.all().count() == 2
    
    @pytest.mark.django_db
    def test_subscription_business_logic(self):
        user = BaseUser.objects.create_user(
            email='user@example.com',
            password='1234@example.com'
        )
        user1 = BaseUser.objects.create_user(
            email='user1@example.com',
            password='1234@example.com'
        )
        user2 = BaseUser.objects.create_user(
            email='user2@example.com',
            password='1234@example.com'
        )
        subscribe(user=user, email=user1)
        subscribe(user=user, email=user2)

        subscribers = get_subscribers(user=user)
        assert len(subscribers) == 2

        unsubscribe(user=user, email=user1)

        subscribers = get_subscribers(user=user)
        assert len(subscribers) == 1

