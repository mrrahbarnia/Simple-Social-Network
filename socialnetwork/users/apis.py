from django.core.validators import MinLengthValidator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    serializers,
    status
)
from drf_spectacular.utils import extend_schema

from api.mixins import ApiAuthMixin
from .selectors import get_profile
from .services import register
from .models import (
    BaseUser,
    Profile
)
from .validators import (
    number_validator,
    letter_validator,
    special_char_validator
)


class ProfileApiView(ApiAuthMixin, APIView):


    class OutputProfileSerializer(serializers.ModelSerializer):

        class Meta:
            model = Profile
            fields = (
                'bio', 'posts_counter',
                'subscribers_count', 'subscriptions_count'
            )
    
    @extend_schema(responses=OutputProfileSerializer)
    def get(self, request, *args, **kwargs):
        try:
            profile_obj = get_profile(user=request.user)
        except Exception as ex:
            return Response(
                {'response': f'Database error {ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = self.OutputProfileSerializer(
            profile_obj, context={'request': request}
        ).data
        return Response(response, status=status.HTTP_200_OK)


class RegisterApiView(APIView):


    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(
            validators=[
                MinLengthValidator(limit_value=10),
                number_validator,
                letter_validator,
                special_char_validator
            ]
        )
        confirm_password = serializers.CharField(max_length=255)
        bio = serializers.CharField(max_length=1000, required=False)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'The provided email has already been taken.'
                )
            return email

        def validate(self, attrs):
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError(
                    'Passwords are not equal...'
                )
            return attrs


    class OutputRegisterSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = BaseUser
            fields = ('email', )

    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register(
                serializer.validated_data.get('email'),
                serializer.validated_data.get('password'),
                serializer.validated_data.get('bio')
            )
        except Exception as ex:
            return Response(
                {'response': f'Database error {ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = self.OutputRegisterSerializer(user, context={'request': request}).data
        return Response(response, status=status.HTTP_200_OK)
