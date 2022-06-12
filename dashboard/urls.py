from urllib.parse import urlsplit
from django.urls import path
from dashboard import views

urlpatterns = [
    path('dashboard/home/', views.DashboardHome, name='d-home'),
    path('dashboard/add-new-item/', views.AddNewItem, name='add-item'),
    path('dashboard/catalog/', views.Catalog, name='catalog'),
    path('dashboard/comments/', views.Comments, name='comments'),
    path('dashboard/edit-user/', views.EditUser, name='edit-user'),
    path('dashboard/users/', views.AllUsers, name='users'),
    path('dashboard/reviews/', views.Reviews, name='reviews'),
    path('dashboard/not-found/', views.NotFound, name='not-found'),
    path('dashboard/users/user/ban-user/<str:email>/', views.BanUser, name='ban-user'),
    path('dashboard/catalog/user/draft-post/series/<str:name>/', views.DraftPostSeries, name='draft-post-series'),
    path('dashboard/catalog/user/draft-post/movies/<str:name>/', views.DraftPostMovies, name='draft-post-movies'),
]