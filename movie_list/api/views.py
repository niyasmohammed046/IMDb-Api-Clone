from movie_list.models import Movie
from movie_list.api. serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET','POST'])
def movies_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def movie_details(request,id):

    if request.method == 'GET':
        movie = Movie.objects.get(id=id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        movie = Movie.objects.get(id=id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'DELETE':
        movie = Movie.objects.get(id=id)
        movie.delete()
        return Response("item deleted",status=status.HTTP_204_NO_CONTENT)