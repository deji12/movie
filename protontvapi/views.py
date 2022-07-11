from django.shortcuts import render
from rest_framework.decorators import api_view
from movieapp.models import movie, series, episode, photos, season, Category
from .serializers import GetAllMoviesSerializer, GetAllSeriesSerializer, GetAllEpisodesSerializer, GetAllPhotosSerializer, GetAllSeasonsSerializer, GetAllGenresSerializer
from rest_framework.response import Response

@api_view(['GET'])
def home(request):
    return Response({
        'To get all movies': 'protontv.cc/api/all-movies/',
        'To get a particular movie': 'protontv.cc/api/get-movie/movie name/',
        'To get all series': 'protontv.cc/api-all-series/',
        'To get a particular series': 'protontv.cc/api/get-series/series name/',
        'To get all series seasons':  'protontv.cc/api/all-series-seasons/',
        'To get all series episodes': 'protontv.cc/api/all-series-episodes/',
        'To get all genres': 'protontv.cc/api/all-genres/',
        'To get all thumbnails': 'protontv.cc/api/all-thumbnails/',
    })

@api_view(['GET'])
def Movies(request):
    all_movies = movie.objects.all()
    serializer = GetAllMoviesSerializer(all_movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Series(request):
    all_series = series.objects.all()
    serializer = GetAllSeriesSerializer(all_series, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Episodes(request):
    all_episodes = episode.objects.all()
    serializer = GetAllEpisodesSerializer(all_episodes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Photos(request):
    all_photos = photos.objects.all()
    serializer = GetAllPhotosSerializer(all_photos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Photos(request):
    all_photos = season.objects.all()
    serializer = GetAllSeasonsSerializer(all_photos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Genres(request):
    all_genres = Category.objects.all()
    serializer = GetAllGenresSerializer(all_genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetMovie(request, name):
    mov = movie.objects.get(name=name)
    serializer = GetAllMoviesSerializer(mov, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def GetSeries(request, name):
    serie = series.objects.get(name=name)
    serializer = GetAllSeriesSerializer(serie, many=False)
    return Response(serializer.data)