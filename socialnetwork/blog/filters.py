from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from rest_framework.exceptions import APIException
from django_filters import (
    FilterSet,
    CharFilter
)

from .models import Post


class PostFilter(FilterSet):

    full_text_search__title = CharFilter(method='filter_full_text_search__title')
    create_at__range = CharFilter(method='filter_create_at__range')
    author__in = CharFilter(method='filter_author__in')
    content__icontains = CharFilter(method='filter_content__icontains')

    def filter_full_text_search__title(self, queryset, name, value):
        return queryset.annotate(
            search=SearchVector('title')).filter(search=value
        )

    def filter_create_at__range(self, queryset, name, value):
        limit = 2
        created_at__range = value.split(',')
        if len(created_at__range) > limit:
            raise APIException(
                "Please just add two created_at with comma separated.\
                    ('2023, 2, 15', '2024, 2, 15') OR ('2023, 2, 15', '') OR ('', '2024, 2, 15')"
            )

        created_at_0, created_at_1 = created_at__range

        if not created_at_1:
            created_at_1 = timezone.now()
        
        if not created_at_0:
            return queryset.filter(created_at__date__lt=created_at_1)
        
        return queryset.filter(created_at__date__range=(created_at_0, created_at_1))

    def filter_author__in(self, queryset, name, value):
        limit = 10 # Business logic: It can also handle in settings.
        author__in = value.split(',')
        if len(author__in) > limit:
            raise APIException(
                f"Cannot input more than {limit} authors."
            )
        return queryset.filter(author__email__in=author__in)

    def filter_content__icontains(self, queryset, name, value):
        return queryset.filter(content__icontains=value)


    class Meta:
        model = Post
        fields = [
            'slug',
            'title'
        ]
