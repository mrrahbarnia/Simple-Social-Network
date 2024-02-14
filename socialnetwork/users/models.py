from django.db import models
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager as BUM
)
from django.contrib.auth.models import PermissionsMixin

from socialnetwork.common.models import BaseModel


class BaseUserManager(BUM):

    def create_user(self, email, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='email address', unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email
    
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, related_name='profile'
    )
    posts_count = models.PositiveIntegerField(default=0)
    subscribers_count = models.PositiveIntegerField(default=0)
    subscriptions_count = models.PositiveIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.email} >> {self.bio}'
