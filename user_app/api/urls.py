from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import registation_view ,logout_view

urlpatterns = [
    #token authentication
    path('register/',registation_view,name="register"),
    path('login/',obtain_auth_token,name="login"),
    path('logout/',logout_view,name="logout"),
]