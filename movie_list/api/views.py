from rest_framework.permissions import IsAuthenticated
from .permissions import AdminOrReadOnly ,ReviewUserOrReadOnly
#viewset and routers imports
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
#class based imports
from movie_list.models import WatchList ,StreamingPlatform
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from movie_list.api. serializers import WatchListSerializer ,StreamingPlatformSerializer

#Generic views import
from rest_framework import generics
from movie_list.models import Review
from . serializers import ReviewSerializer
from rest_framework.exceptions import ValidationError

# Generic views(concrete view class)
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

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

class ReviewList(generics.ListAPIView):  # this has post and get
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView): # this has get,update and delete
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


# #Generic views imports (mixins)
# from rest_framework import mixins,generics
# from movie_list.models import Review
# from . serializers import ReviewSerializer

# #Generic views (mixins)
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request ,*args , **kwargs):
#         return self.list(request ,*args , **kwargs)
    
#     def post(self,request,*args ,**kwargs):
#         return self.create(request,*args ,**kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request ,*args , **kwargs):
#         return self.retrieve(request ,*args , **kwargs)


#ModelViewSet
class StreamingPlatformVS(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer


#viewset and routers
# class StreamingPlatformVS(viewsets.ViewSet):

#     def list(self,request):
#         queryset = StreamingPlatform.objects.all()
#         serializer = StreamingPlatformSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamingPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamingPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer = StreamingPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)



#Class Based views

class StreamingPlatformAV(APIView):
    def get(self,request):
        platform  = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(platform,many=True,context= {'request':request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatformDeatilsAV(APIView):

    def get (self,request,id,):
        try:
            platform = StreamingPlatform.objects.get(id=id)
        except StreamingPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self,request,id):
        platform = StreamingPlatform.objects.get(id=id)
        serializer = StreamingPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self,request,id):
        platform = StreamingPlatform.objects.get(id=id)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchListAV(APIView):
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




#FUNCTION BASED VIEWS

# from movie_list.models import Movie
# from movie_list.api. serializers import MovieSerializer
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status

# @api_view(['GET','POST'])
# def movies_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,id):

    # if request.method == 'GET':
    #     try:
    #         movie = Movie.objects.get(id=id)
    #     except Movie.DoesNotExist:
    #         return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
    #     serializer = MovieSerializer(movie)
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    
    # if request.method == 'PUT':
    #     movie = Movie.objects.get(id=id)
    #     serializer = MovieSerializer(movie, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(id=id)
#         movie.delete()
#         return Response("item deleted",status=status.HTTP_204_NO_CONTENT)