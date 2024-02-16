from django.urls import path
from .apis.post import (
    PostAPiView,
    PostDetailApiView
)

urlpatterns = [
    path('post/', PostAPiView.as_view(), name='post_list'),
    path('post/<slug:slug>', PostDetailApiView.as_view(), name='post_detail'),
]
