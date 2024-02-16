from django.urls import path, include

urlpatterns = [
    path('jwt/', include(('socialnetwork.authentication.urls', 'jwt'))),
    path('users/', include(('socialnetwork.users.urls', 'users'))),
    path('blog/', include(('socialnetwork.blog.urls', 'blog'))),

]
