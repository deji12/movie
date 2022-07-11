from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('all-movies/', views.Movies),
    path('all-series/', views.Series),
    path('all-series-episodes/', views.Episodes),
    path('all-thumbnails/', views.Photos),
    path('all-series-seasons/', views.Photos),
    path('all-genres/', views.Genres),
    path('get-movie/<str:name>/', views.GetMovie),
    path('get-series/<str:name>/', views.GetSeries),
]