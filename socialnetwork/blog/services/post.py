from django.db import transaction
from django.utils.text import slugify
from rest_framework.exceptions import APIException

from socialnetwork.users.models import BaseUser
from ..models import Post
from .caches import profile_cache

@transaction.atomic
def create_post(*, user:BaseUser, title:str, content:str) -> Post:
    post = Post.objects.create(
        slug=slugify(title),
        author=user,
        title=title,
        content=content
    )
    profile_cache(user=user)
    return post

@transaction.atomic
def delete_post(*, user:BaseUser, slug:str) -> None:
    try:
        Post.objects.get(author=user, slug=slug).delete()
    except Post.DoesNotExist:
        raise APIException(
            'There is no post with the provided slug.'
        )
    profile_cache(user=user)
