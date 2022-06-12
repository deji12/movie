from django.shortcuts import render, redirect
from movieapp.models import movie, series, Profile, comment, reviewss, episode_review, episode_comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your views here.

def DashboardHome(request):
    all_movies = movie.objects.all().order_by('-clicks')[:5]
    all_series = series.objects.all().order_by('-clicks')[:5]
    new_movies = movie.objects.all().order_by('-date_added')[:5]
    new_series = series.objects.all().order_by('-series_air_date')[:5]
    new_reviews = episode_review.objects.all().order_by('-date')[:5]
    all_users = User.objects.all().order_by('-username')[:5]

    final = 0
    for i in comment.objects.all():
        final+=1
    for j in episode_comment.objects.all():
        final+=1

    final_review_num = 0
    for i in reviewss.objects.all():
        final_review_num+=1
    
    for j in episode_review.objects.all():
        final_review_num+=1

    context = {
        'movies': all_movies, 
        'series': all_series,
        'new_movies': new_movies,
        'new_series': new_series,
        'new_review': new_reviews,
        'users': all_users,
        'total_comments': final,
        'total_reviews': final_review_num,
    }
    return render(request, 'dashboard/index.html', context)

def Catalog(request):
    all_movies = movie.objects.all().order_by('-clicks')
    all_series = series.objects.all().order_by('-clicks')
    final = 0
    for i in all_movies:
        final+=1
    for j in all_series:
        final+=1
    context = {
        'movies': all_movies, 
        'series': all_series,
        'content': final
    }
    return render(request, 'dashboard/catalog.html', context)

def AllUsers(request):
    all_users = Profile.objects.all()
    user_number = 0
    for i in all_users:
        user_number+=1

    
    
    context = {
        'all_users': all_users,
        'user_num': user_number,
    }
    return render(request, 'dashboard/users.html', context)

def Comments(request):
    context = {
        
    }
    return render(request, 'dashboard/comments.html', context)

def Reviews(request):
    context = {
        
    }
    return render(request, 'dashboard/reviews.html', context)

def NotFound(request):
    context = {
        
    }
    return render(request, 'dashboard/pages.html', context)

def AddNewItem(request):
    context = {
        
    }
    return render(request, 'dashboard/add-item.html', context)

def EditUser(request):
    context = {
        
    }
    return render(request, 'dashboard/edit-user.html', context)

def BanUser(request, email):
    get_profile = Profile.objects.get(email=email) 
    if get_profile.verified == True:
        get_profile.verified = False
        get_profile.save()
        return redirect('users')
    else:
        get_profile.verified = True
        get_profile.save()
        return redirect('users')

def DraftPostSeries(request, name):
    get_series = series.objects.get(name=name)
    if get_series.draft == False:
        get_series.draft = True
        get_series.save()
        return redirect('catalog')
    else:
        get_series.draft = False
        get_series.save()
        return redirect('catalog')
    

def DraftPostMovies(request, name):
    get_movie = movie.objects.get(name=name)
    if get_movie == False:
        get_movie.draft = True
        get_movie.save()
        return redirect('catalog')
    else:
        get_movie.draft = False
        get_movie.save()
        return redirect('catalog')