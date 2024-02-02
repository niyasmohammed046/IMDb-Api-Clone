from rest_framework.routers import DefaultRouter
from django.urls import include
from django.urls import path
from.views import (WatchListAV ,WatchDetailAV ,ReviewList ,ReviewDetail,
                   ReviewCreate,StreamingPlatformVS,UserReview )

router = DefaultRouter()
router.register('stream',StreamingPlatformVS,basename='streamplatform')

urlpatterns = [

    path('',WatchListAV.as_view(),name='movie-list'),
    path('<int:id>/',WatchDetailAV.as_view(),name='movie-detail'),

    path('',include(router.urls)),

    path('<int:pk>/review/create/',ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/reviews/',ReviewList.as_view(),name='review-list'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),

    path('user-reviews/',UserReview.as_view(),name='user-review')

]