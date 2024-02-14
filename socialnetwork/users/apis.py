from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    serializers,
    status
)
from drf_spectacular.utils import extend_schema

from .models import BaseUser


class RegisterApiView(APIView):


    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=255)
        confirm_password = serializers.CharField(max_length=255)


    class OutputRegisterSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = BaseUser
            fields = ('email', )

    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_user(
                serializer.validated_data.get('email'),
                serializer.validated_data.get('password')
            )
        except Exception as ex:
            return Response(
                {'response': f'Database error {ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = self.OutputRegisterSerializer(query, context={'request': request}).data
        return Response(response)
