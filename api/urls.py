from django.urls import path, include
from django.conf.urls import url 
from knox.views import LogoutView
from .views import HelloAPI,RegistrationAPI, LoginAPI, UserAPI, PostListAPI, PostDetailAPI, PostFavoriteAPI, PostFavoriteListAPI

urlpatterns=[
	path("hello/",HelloAPI),
	path("auth/register/", RegistrationAPI.as_view()),
    path("auth/login/", LoginAPI.as_view()),
    path("auth/user/", UserAPI.as_view()),
    path("list/", PostListAPI.as_view()),
    path("detail/<int:pk>/",PostDetailAPI.as_view()),
    path("auth/logout/", LogoutView.as_view(), name='knox_logout'),
    path("favorite/<int:pk>/", PostFavoriteAPI.as_view()),
    path("favorite/",PostFavoriteListAPI.as_view()),
]