from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/watch/',include('movie_list.api.urls')),
    path('api/account/',include('user_app.api.urls')),
]