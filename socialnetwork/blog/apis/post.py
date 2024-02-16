from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    serializers,
    status
)
from drf_spectacular.utils import extend_schema

from socialnetwork.api.mixins import ApiAuthMixin
from socialnetwork.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response_context
)

from ..services.post import create_post
from ..selectors.post import post_list
from ..models import (
    Post,
    Subscription
)


class PostAPiView(ApiAuthMixin, APIView):


    class Pagination(LimitOffsetPagination):
        default_limit = 10

    
    class FilterSerializer(serializers.Serializer):
        full_text_search__title = serializers.CharField(
            required=False, max_length=100
        )
        created_at__range = serializers.CharField(
            required=False, max_length=100
        )
        author__in = serializers.CharField(
            required=False, max_length=100
        )
        slug = serializers.CharField(required=False, max_length=100)
        title = serializers.CharField(required=False, max_length=100)
        content__icontains = serializers.CharField(required=False, max_length=1000)


    class InputPostSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        content = serializers.CharField(max_length=1000)


    class OutputPostSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField()
        # absolute_url = serializers.SerializerMethodField()

        class Meta:
            model = Post
            fields = ('title', 'content', 'author',)
        
        def get_author(self, post):
            return post.author.email

        # def get_absolute_url(self, post):
        #     request = self.context.get('request')
        #     path = reverse('api:blog:post_detail', args=[post.slug])
        #     return request.build_absolute_uri(path)

    @extend_schema(
            parameters=[FilterSerializer],
            responses=OutputPostSerializer
    )
    def get(self, request, *args, **kwargs):
        filtered_serializer = self.FilterSerializer(data=request.query_params)
        filtered_serializer.is_valid(raise_exception=True)
        try:
            queryset = post_list(
                user = request.user,
                filters = filtered_serializer.validated_data
            )
        except Exception as ex:
            return Response(
                {'response': f'Database error => {ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutputPostSerializer,
            queryset=queryset,
            request=request,
            view=self
        )
    
    @extend_schema(
            request=InputPostSerializer,
            responses=OutputPostSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = create_post(
                author = request.user,
                title = serializer.validated_data.get('title'),
                content = serializer.validated_data.get('content')
            )
        except Exception as ex:
            return Response(
                {'response': f'Database error => {ex}'}
            )

        response = self.OutputPostSerializer(post, context={'request': request}).data
        return Response(
            response,
            status=status.HTTP_201_CREATED
        )


class PostDetailApiView(ApiAuthMixin, APIView):
    pass
