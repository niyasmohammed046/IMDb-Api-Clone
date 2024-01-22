# from django.shortcuts import render
# from .models import Movie
# from django.http import JsonResponse


# def movies_list(request):
#     movies = Movie.objects.all()
#     context = {
#         'movies':list(movies.values())
#     }
#     return JsonResponse(context)

# def movie_details(request,id):
#     movie = Movie.objects.get(id=id)
#     context = {
#         'name':movie.name,
#         'desc':movie.description,
#         'active':movie.active
#     }
#     return JsonResponse(context)