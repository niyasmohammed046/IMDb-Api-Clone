from django.urls import path
from . import views

urlpatterns = [
    path('',views.movies_list,name="movies_list"),
    path('movie_details/<int:id>/',views.movie_details,name="movie_details"),
]