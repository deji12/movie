from urllib.parse import urlsplit
from django.urls import path
from dashboard import views

urlpatterns = [
    path('dashboard/home/', views.DashboardHome, name='d-home'),
    path('dashboard/add-new-item/', views.AddNewItem, name='add-item'),
    path('dashboard/catalog/', views.Catalog, name='catalog'),
    path('dashboard/comments/', views.Comments, name='comments'),
    path('dashboard/edit-user/<str:email>/', views.EditUser, name='edit-user'),
    path('dashboard/edit-user/<str:email>/comments/delete/<str:name>/<str:title>/<str:series_name>/<str:comment_content>/', views.DeleteCommentSeries, name='edit-user2'),
    path('dashboard/users/', views.AllUsers, name='users'),
    path('dashboard/reviews/', views.Reviews, name='reviews'),
    path('dashboard/not-found/', views.NotFound, name='not-found'),
    path('dashboard/users/user/ban-user/<str:email>/', views.BanUser, name='ban-user'),
    path('dashboard/catalog/user/draft-post/series/<str:name>/', views.DraftPostSeries, name='draft-post-series'),
    path('dashboard/catalog/user/draft-post/movies/<str:name>/', views.DraftPostMovies, name='draft-post-movies'),
    path('dashboard/comments/delete/<str:name>/<str:title>/<str:series_name>/<str:comment_content>/', views.DeleteCommentSeries, name='delete-comment-series'),
    path('dashboard/comments/delete-movie/<str:name>/<str:movie_name>/<str:body>/', views.DeleteCommentMovies, name='delete-comment-movie'),
    path('dashboard/reviews/delete-movie-review/<str:name>/<str:movie_name>/<str:body>/', views.DeleteReviewMovies, name='delete-review-movie'),
    path('dashboard/reviews/delete-series-review/<str:name>/<str:title>/<str:series_name>/<str:comment_content>/', views.DeleteReviewSeries, name='delete-review-series'),
    path('dashboard/users/edit-user-profile/<str:email>/', views.EditProfileDetails, name='edit-user-profile'),
    path('dashboard/users/change-user-password/<str:email>/', views.ChangePassword, name='change-user-password'),
    path('dashboard/catalog/search/', views.search, name='search-catalog'),
    path('dashboard/catalog/filter-by-date-created/', views.Date_Created, name='filter-created'),
    path('dashboard/catalog/filter-by-user-date-creation/', views.DateUserCreated, name='filter-date-created'),
    path('dashbboard/users/filter-verified-users/', views.VerifiedUsers, name='verified-users'),
    path('dashbboard/users/filter-banned-users/', views.BannedUsers, name='banned-users'),
    path('dashboard/comments/filter-user-comments/', views.FilterCommentsSeries, name='filter-comment-series'),
    path('dashboard/comments/filter-user-reviews/', views.FilterReviews, name='filter-comment-reviews'),
]