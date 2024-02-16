from django.urls import path
from .apis.post import PostAPiView

urlpatterns = [
    path('post/', PostAPiView.as_view(), name='post_list'),

]
