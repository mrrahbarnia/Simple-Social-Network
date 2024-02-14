import pytest

from .services import create_user
from .models import BaseUser


class TestUserBusinessLogic:

    def test_create_user_business_logic(self):
        email = 'example@gmail.com'
        password = 'example@example12345'

        create_user(email=email, password=password)

        sample_user = BaseUser.objects.filter(email=email).exists()

        assert sample_user == True


