from django.shortcuts import render, redirect
from movieapp.models import movie, series, Profile, comment, reviewss, episode_review, episode_comment, episode
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate

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
    series_comment = episode_comment.objects.all()
    movie_comment = comment.objects.all()
    context = {
        'series': series_comment,
        'movie': movie_comment,
    }
    return render(request, 'dashboard/comments.html', context)

def DeleteCommentSeries(request, name, title, series_name, comment_content, email):
    get_user = User.objects.get(username=name)
    get_profile = Profile.objects.get(user=get_user)
    get_series = series.objects.get(name=series_name)
    get_episode = episode.objects.get(title=title, series_name=get_series)
    get_episode_comment = episode_comment.objects.get(name=get_user, episode=get_episode, series_name=get_series, body=comment_content)
    get_episode_comment.delete()
    get_profile.comments -=1
    get_profile.save()
    return redirect('comments')

def DeleteCommentMovies(request, name, movie_name, body):
    get_user = User.objects.get(username=name)
    get_profile = Profile.objects.get(user=get_user)
    get_movie = movie.objects.get(name=movie_name)
    get_movie  = comment.objects.get(name=get_user, movie=get_movie,  body=body)
    get_movie.delete()
    get_profile.comments -=1
    get_profile.save()
    return redirect('comments')

def Reviews(request):
    all_reviews = reviewss.objects.all()
    episode_reviews = episode_review.objects.all()
    num_reviews = 0
    for i in all_reviews:
        num_reviews+=1
    for j in episode_reviews:
        num_reviews+=1

    context = {
        'reviews': all_reviews,
        'episode_review': episode_reviews,
        'num_revs':num_reviews,
    }
    return render(request, 'dashboard/reviews.html', context)

def DeleteReviewMovies(request, name, movie_name, body):
    get_user = User.objects.get(username=name)
    get_profile = Profile.objects.get(user=get_user)
    get_movie = movie.objects.get(name=movie_name)
    get_movie  = reviewss.objects.get(name=get_user, movie=get_movie, body=body)
    get_movie.delete()
    get_profile.reviews -=1
    get_profile.save()
    return redirect('reviews')

def DeleteReviewSeries(request, name, title, series_name, comment_content):
    get_user = User.objects.get(username=name)
    get_profile = Profile.objects.get(user=get_user)
    get_series = series.objects.get(name=series_name)
    get_episode = episode.objects.get(title=title, series_name=get_series)
    get_episode_comment = episode_review.objects.get(name=get_user, episode=get_episode, series_name=get_series, body=comment_content)
    get_episode_comment.delete()
    get_profile.reviews -=1
    get_profile.save()
    return redirect('reviews')

def NotFound(request):
    context = {
        
    }
    return render(request, 'dashboard/pages.html', context)

def AddNewItem(request):
    context = {
        
    }
    return render(request, 'dashboard/add-item.html', context)

def EditUser(request, email):
    get_profile = Profile.objects.get(email=email) 
    get_user = User.objects.get(email=email)

    all_comments_movie = comment.objects.all()
    all_series_comments = episode_comment.objects.all()
    total_comments = 0
    for i in  all_comments_movie:
        total_comments+=1
    for i in all_series_comments:
        total_comments+=1


    series_comment = episode_comment.objects.filter(name=get_user)
    movie_comments  = comment.objects.filter(name=get_user)
    number_of_comment_by_user = 0
    for i in series_comment:
        number_of_comment_by_user+=1

    for i in movie_comments:
        number_of_comment_by_user+=1

    movie_review = reviewss.objects.filter(name=get_user)
    series_reviews = episode_review.objects.filter(name=get_user)
    all_movie_review = reviewss.objects.all()
    all_series_review = episode_review.objects.all()

    user_reviews = 0
    for i in movie_review:
        user_reviews+=1
    for i in series_reviews:
        user_reviews+=1

    all_reviews = 0
    for i in all_series_review:
        all_reviews+=1
    for i in all_series_review:
        all_reviews+=1

    context = {
        'profile': get_profile,
        'episode': series_comment,
        'movie': movie_comments,
        'user_comment': number_of_comment_by_user,
        'number_of_comments': total_comments,
        'movie_review': movie_review,
        'series_review': series_reviews,
        'user_review': user_reviews,
        'number_of_revs': all_reviews,
        'user': get_user,
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


# EDIT USER VIEWS
def EditProfileDetails(request, email):
    get_profile = Profile.objects.get(email=email) 
    get_user = User.objects.get(email=email)
    series_comment = episode_comment.objects.filter(name=get_user)

    if request.method == 'POST':        
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        subscription = request.POST.get('subscription')
        user_type = request.POST.get('user_type')

        if username:
            get_user.username = username
            get_profile.user_name = username
            get_user.save()
        if email:
            get_user.email = email
            get_profile.email = email
            get_user.save()
        if first_name:
            get_user.first_name = first_name
            get_user.save()
        if last_name:
            get_user.last_name = last_name
            get_user.save()
        if subscription:
            get_profile.pricing_plan = subscription
            get_profile.save()
        if user_type:
            if user_type == 'Admin':
                get_user.is_superuser = True
                get_user.save()
            elif user_type == 'User':
                get_user.is_superuser = False
                get_user.save()
        messages.success(request, 'Profile Updated Successfully')
        return render(request, 'dashboard/edit-user.html', {'profile': get_profile})

    return render(request, 'dashboard/edit-user.html', {'profile': get_profile, 'episode': series_comment})


def ChangePassword(request, email):
    get_user = User.objects.get(email=email)
    get_profile = Profile.objects.get(email=email)
    
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpass')
        newpassword = request.POST.get('newpass')
        confirmpassword = request.POST.get('confirmpass')

        if len(confirmpassword) < 5:
            messages.success(request, 'Password too short')
            return render(request, 'dashboard/edit-user.html', {'profile': get_profile})

        auth_user = authenticate(username=get_user.username, password=oldpassword)
       
        if auth_user is not None:
            if confirmpassword != newpassword:
                messages.success(request, 'Passwords do not match')
                return render(request, 'dashboard/edit-user.html', {'profile': get_profile})
            else:
                get_user.set_password(confirmpassword)
                get_user.save()
                messages.success(request, 'Password changed successfully')
                return render(request, 'dashboard/edit-user.html', {'profile': get_profile})
        else:
            messages.success(request, 'Error, wrong details')
            return render(request, 'dashboard/edit-user.html', {'profile': get_profile})

       
def search(request):
    if request.method == 'POST':
        search_val = request.POST.get('search')
        user_search = request.POST.get('search-user')
        print(user_search)
        if user_search:
            if '@' in user_search:
                search_for_user_by_email = Profile.objects.filter(email=user_search)
                print(search_for_user_by_email)
                context = {
                    'all_users': search_for_user_by_email,
                    'search': user_search,
                }
                return render(request, 'dashboard/users.html', context)

            else:
                search_for_user_by_username = Profile.objects.filter(user_name=user_search)
                print(search_for_user_by_username)
                context = {
                    'all_users': search_for_user_by_username,
                    'search': user_search,
                }
                return render(request, 'dashboard/users.html', context)

        if search_val:
            filter_movie_for_search = movie.objects.filter(name__icontains=search_val)
            filter_series_for_search = series.objects.filter(name__icontains=search_val)

            final = 0
            for i in filter_movie_for_search:
                final+=1
            for i in filter_series_for_search:
                final+=1

            context = {
                'movie_result': filter_movie_for_search,
                'series_result': filter_series_for_search,
                'search': search_val,
                'final': final,
            }
            return render(request, 'dashboard/search.html', context)


def Date_Created(request):
    all_movies = movie.objects.all().order_by('-date_added')
    all_series = series.objects.all().order_by('-series_air_date')
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

def DateUserCreated(request):
    all_users = Profile.objects.all().order_by('-creation_date')
    user_number = 0
    for i in all_users:
        user_number+=1
    
    context = {
        'all_users': all_users,
        'user_num': user_number,
    }
    return render(request, 'dashboard/users.html', context)

def VerifiedUsers(request):
    all_users = Profile.objects.filter(verified=True)
    user_number = 0
    for i in all_users:
        user_number+=1
    
    context = {
        'all_users': all_users,
        'user_num': user_number,
    }
    return render(request, 'dashboard/users.html', context)

def BannedUsers(request):
    all_users = Profile.objects.filter(verified=False)
    user_number = 0
    for i in all_users:
        user_number+=1
    
    context = {
        'all_users': all_users,
        'user_num': user_number,
    }
    return render(request, 'dashboard/users.html', context)

def FilterCommentsSeries(request):
    if request.method == 'POST':
        search_val = request.POST.get('search')
        user = User.objects.get(username=search_val)
        series_comment = episode_comment.objects.filter(name=user)
        movie_comment = comment.objects.filter(name=user)
        context = {
                'series': series_comment,
                'movie': movie_comment,
                'search': search_val,
            }
        return render(request, 'dashboard/comments.html', context)
        # try:
        #     user = User.objects.get(username=user)
        #     series_comment = episode_comment.objects.filter(name__icontains=user)
        #     movie_comment = comment.objects.filter(name__icontains=search)
        #     context = {
        #         'series': series_comment,
        #         'movie': movie_comment,
        #         'search': search_val,
        #     }
        #     return render(request, 'dashboard/comments.html', context)
        # except:
        #     messages.success(request, f'| User {search_val} does not exist')
        #     return render(request, 'dashboard/comments.html')