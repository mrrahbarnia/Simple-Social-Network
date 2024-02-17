from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    serializers,
    status
)
from drf_spectacular.utils import extend_schema

from socialnetwork.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response_context
)
from socialnetwork.api.mixins import ApiAuthMixin
from ..models import Subscription
from ..services.subscription import (
    subscribe,
    unsubscribe
)
from ..selectors.subscription import get_subscribers 


class SubscriptionApiView(ApiAuthMixin, APIView):
    

    class Pagination(LimitOffsetPagination):
        limit = 20


    class InputSubscriptionSerializer(serializers.Serializer):
        email = serializers.EmailField()


    class OutPutSubscriptionSerializer(serializers.ModelSerializer):
        email = serializers.SerializerMethodField()

        class Meta:
            model = Subscription
            fields = ('email',)
        
        def get_email(self, subscription):
            return subscription.target.email

    @extend_schema(
            responses=OutPutSubscriptionSerializer
    )
    def get(self, request, *args, **kwargs):
        try:
            subscribers = get_subscribers(user=request.user)
        except Exception as ex:
            return Response(
                {'response': f'Database error => {ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutSubscriptionSerializer,
            queryset=subscribers,
            request=request,
            view=self
        )

    @extend_schema(
            request=InputSubscriptionSerializer,
            responses=OutPutSubscriptionSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = subscribe(
                user=request.user, email=serializer.validated_data.get('email')
            )
        except Exception as ex:
            return Response(
                {'response': f'Database error => {ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response = self.OutPutSubscriptionSerializer(query).data
        return Response(
            response,
            status=status.HTTP_200_OK
        )


class SubscriptionDetailApiView(ApiAuthMixin, APIView):

    def delete(self, request, email, *args, **kwargs):
        try:
            query = unsubscribe(user=request.user, email=email)
        except Exception as ex:
            return Response(
                {'response': f'Database error => {ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status.HTTP_204_NO_CONTENT)
