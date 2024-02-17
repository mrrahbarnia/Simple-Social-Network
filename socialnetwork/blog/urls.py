from django.urls import path
from .apis.post import (
    PostAPiView,
    PostDetailApiView
)
from .apis.subscription import (
    SubscriptionApiView,
    SubscriptionDetailApiView
)

urlpatterns = [
    path('post/', PostAPiView.as_view(), name='post_list'),
    path('post/<slug:slug>', PostDetailApiView.as_view(), name='post_detail'),
    path('subscribe/', SubscriptionApiView.as_view(), name='subscribe_list'),
    path('unsubscribe/<str:email>/', SubscriptionDetailApiView.as_view(), name='subscribe_detail'),
]
