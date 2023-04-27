from django.urls import path,include
from .views import home,register,create_post,create_userPp,login_view,like
urlpatterns = [
    path('home',home,name="home"),
    path('register',register,name="register"),
    path('create_post',create_post,name="create_post"),
    path('userProfile',create_userPp,name="userProfile"),
    path('login',login_view,name="login"),
    path('like<int:pk>',like,name='like'),
]