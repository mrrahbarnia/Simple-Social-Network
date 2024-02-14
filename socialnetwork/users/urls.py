from django.urls import path

from .apis import (
    RegisterApiView,
    ProfileApiView
)

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('profile/', ProfileApiView.as_view(), name='profile')
]
