import pytest

from .selectors import get_profile
from .services import register
from .models import (
    BaseUser,
    Profile
)


class TestUserBusinessLogic:

    @pytest.mark.django_db
    def test_user_business_logics(self):
        email = 'example@gmail.com'
        password = 'example@example12345'

        register(email=email, password=password, bio=None)

        sample_user = BaseUser.objects.get(email=email)
        sample_profile = Profile.objects.get(user=sample_user)

        selected_profile = get_profile(user=sample_user)

        assert sample_user,email == 'example@gmail.com'
        assert sample_profile.user == sample_user
        assert selected_profile == sample_profile
