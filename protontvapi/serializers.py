from rest_framework import serializers
from movieapp import models

class GetAllMoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.movie
        fields = ['name', 'info', 'thumbnail', 'age', 'genre1', 'genre2', 'rating', 'year', 'country', 'video', 'duration']

class GetAllSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.series
        fields = '__all__'

class GetAllEpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.episode
        fields = ['title', 'series_name', 'season_val', 'episode_num', 'video', 'duration']

class GetAllPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.photos
        fields = '__all__'      

class GetAllSeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.season
        fields = ['id', 'season_num', 'series_name']


class GetAllGenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__' 