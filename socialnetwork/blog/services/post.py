from django.utils.text import slugify

from ..models import Post
from socialnetwork.users.models import BaseUser

def create_post(*, user:BaseUser, title:str, content:str) -> Post:
    return Post.objects.create(
        slug=slugify(title),
        author=user,
        title=title,
        content=content
    )
