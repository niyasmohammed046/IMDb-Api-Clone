from .throttling import ReviewCreateThrottle,ReviewListThrottle
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly ,ReviewUserOrReadOnly
from rest_framework import viewsets
from movie_list.models import WatchList ,StreamingPlatform
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from movie_list.api. serializers import WatchListSerializer ,StreamingPlatformSerializer
from rest_framework.throttling import AnonRateThrottle , ScopedRateThrottle
from rest_framework import generics
from . serializers import ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from movie_list.models import Review
from . serializers import ReviewSerializer
from rest_framework.exceptions import ValidationError



class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("you have already reviewed this movie")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating'] # this means if no of rating is 0 show the rating
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) /2  #this is taking the old + new value then /2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist ,review_user=review_user)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


#ModelViewSet                                   (route in urls)
class StreamingPlatformVS(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,id):
        try:
            movie = WatchList.objects.get(id=id)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,id):
        movie = WatchList.objects.get(id=id)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,id):
        movie=WatchList.objects.get(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)