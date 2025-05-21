from django.urls import path,re_path
from .views import  UserProfileView,UserDetaView,Register

urlpatterns = [
    path('profile/',UserProfileView.as_view(),name='user_profile'),
    path('user/',Register.as_view(),name='users'),
    re_path('user/(?P<pk>\d+)',UserDetaView.as_view(),name='userdata')
]