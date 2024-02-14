from django.urls import path, include

urlpatterns = [
    path('jwt/', include('socialnetwork.authentication.urls')),
    path('users/', include('socialnetwork.users.urls')),
]
