from turtle import title
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #Allow other domains access our api method
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Movies
from rest_framework.filters import OrderingFilter
from .serializers import MovieSerializer
import serializers
from django.db.models import Q 
import math


# Create your views here.

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_movie(request, format=None):
    page = int(request.GET.get('page', 1))
    per_page = 25

    movies= Movies.objects.all()
    total = movies.count()
    start = (page - 1) * per_page
    end = page * per_page

    search_serializer = MovieSerializer(movies[start:end], many=True)
    return Response({
        "Movies":search_serializer.data,
        "total": total,
        "page": page,
        "last_page": math.ceil(total / per_page)
        })
    

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def movie_detail(request, id, format=None):

    try:
        movie = Movies.objects.get(pk=id)
    except Movies.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET',])
def search_movie(request): #http://127.0.0.1:8000/api/movies/search?s=Jai
    s = request.GET.get('s')
    page = int(request.GET.get('page', 1))
    per_page = 25

    movies = Movies.objects.all()

    if s:
        movies = movies.filter(Q(Movie_Name__icontains=s) | Q(Movie_Description__icontains=s))


    total = movies.count()
    start = (page - 1) * per_page
    end = page * per_page

    search_serializer = MovieSerializer(movies[start:end], many=True)
    return Response({
        "Movies":search_serializer.data,
        "total": total,
        "page": page,
        "last_page": math.ceil(total / per_page)
        })


@api_view(['GET',])
def sort_movie(request): #http://127.0.0.1:8000/api/movies/sort?sort=desc
    sort = request.GET.get('sort')
    page = int(request.GET.get('page', 1))
    per_page = 25

    movies = Movies.objects.all()

    if sort == 'asc':
        movies = movies.order_by('Movie_Name')
        movies = movies.order_by('Movie_Rating')
        movies = movies.order_by('Year_of_Release')
        movies = movies.order_by('Movie_Duration')

    elif sort == 'desc':
        movies = movies.order_by('-Movie_Name')
        movies = movies.order_by('-Movie_Rating')
        movies = movies.order_by('-Year_of_Release')
        movies = movies.order_by('-Movie_Duration')

    total = movies.count()
    start = (page - 1) * per_page
    end = page * per_page

    search_serializer = MovieSerializer(movies[start:end], many=True)
    return Response({
        "Movies":search_serializer.data,
        "total": total,
        "page": page,
        "last_page": math.ceil(total / per_page)
        })

