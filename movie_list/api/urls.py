from rest_framework.routers import DefaultRouter
from django.urls import include

#CLASS BASED URLS
from django.urls import path
from.views import (WatchListAV ,WatchDetailAV , StreamingPlatformAV ,
                   StreamPlatformDeatilsAV ,ReviewList ,ReviewDetail,
                   ReviewCreate,StreamingPlatformVS )

router = DefaultRouter()
router.register('stream',StreamingPlatformVS,basename='streamplatform')


urlpatterns = [

    path('list/',WatchListAV.as_view(),name='movie_list'),
    path('<int:id>/',WatchDetailAV.as_view(),name='movie-detail'),

    # path('stream/',StreamingPlatformAV.as_view(),name="platform"),
    # path('stream/<int:id>/',StreamPlatformDeatilsAV.as_view(),name="platformdetail"),
    path('',include(router.urls)),

    #mixins and generic view urls
    # path('review/',ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),

    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/review/',ReviewList.as_view(),name='review-list'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),

]





#FUNCTION BASED URLS

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('',views.movies_list,name="movies_list"),
#     path('movie_details/<int:id>/',views.movie_details,name="movie_details"),
# ]