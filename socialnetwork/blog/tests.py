import pytest

from socialnetwork.users.models import BaseUser
from .services.post import create_post
from .selectors.post import (
    post_list,
    post_detail
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

