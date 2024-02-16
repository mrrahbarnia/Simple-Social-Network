from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..common.models import BaseModel

User = get_user_model()


class Post(BaseModel):
    slug = models.SlugField(
        primary_key=True,
        max_length=100
    )
    title = models.CharField(max_length=100, unique=True)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )

    def __str__(self) -> str:
        return self.slug


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sub'
    )
    target = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='targets'
    )
    
    class Meta:
        unique_together = ('subscriber', 'target')
    
    def clean(self) -> None:
        if self.subscriber == self.target:
            raise ValidationError(
                'Subscriber must not be the same with the target user.'
            )

    def __str__(self) -> str:
        return f"{self.subscriber.email} >> {self.target.email}"
