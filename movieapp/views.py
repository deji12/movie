import re
from textwrap import fill
from unicodedata import category
from django.shortcuts import render, redirect
from .models import movie, series
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import comment, reviewss, Category, rate, year, episode, season, series_comment, episode_review as er, episode_comment, photos, Profile
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

import requests

# Create your tests here.
# url = 'https://fmovies-api.herokuapp.com/details?'
# response = requests.get(
#     url,
#     params= 'link=https://fmovies.to/movie/ambulance-lx84n/1-full'
# )
# data = response.json()
# final_mv = []
# for j in range(1):
#     for i in data:
#         final_mv.append(i)
    

def home(request):
    get_movies = movie.objects.all()
    get_series = series.objects.all()
    get_cartoons = movie.objects.filter(cat='cartoon')
    get_premier = movie.objects.filter(premier=True)
    get_premier_series = series.objects.filter(premier=True)
    context = {
        'movie': get_movies,
        'series': get_series,
        'cartoon': get_cartoons,
        'premier': get_premier,
        'series_premier': get_premier_series,
    }
    return render(request, 'movieapp/index.html', context)

def searchresult(request):

    if request.method == 'POST':
        search = request.POST.get('search')
       
        filter_for_movies = movie.objects.filter(name__icontains=search)
        filter_for_series = series.objects.filter(name__icontains=search)


        context = {
                'movie': filter_for_movies,
                'series': filter_for_series,
                'search': search
            }
        return render(request, 'movieapp/search-result.html', context)
    return render(request, 'movieapp/search-result.html')

def detail(request, name):
    if request.method == 'POST':
        if request.user.is_authenticated:
            get_profile = Profile.objects.get(user=request.user)
            title = request.POST.get('title')
            review = request.POST.get('review')
            text = request.POST.get('body')
            rate = request.POST.get('rate')

            if text:
                new_comment = comment(name=request.user, body=text)
                new_comment.movie = movie.objects.get(name=name)
                new_comment.save()
                get_profile.comments +=1
                get_profile.save()
                return redirect('detail', name=name)
            if title:
                new_review = reviewss(name=request.user, title=title, body=review, rate=rate)
                new_review.movie = movie.objects.get(name=name)
                get_profile.reviews +=1
                get_profile.save()
                new_review.save()
                return redirect('detail', name=name)
        else:
            messages.error(request, 'Please signin to post a comment or review')
            return redirect('detail', name=name)    

    mov = movie.objects.get(name=name)
    mov.clicks +=1
    mov.save()
    pics = photos.objects.filter(movie_name=mov)
    all_movies = movie.objects.all()
    all_coms = comment.objects.filter(movie=mov)
    all_reviews = reviewss.objects.filter(movie=mov)
    get_movie = movie.objects.get(name=name)

    context = {
        'movie': get_movie,
        'al': all_movies,
        'coms': all_coms,
        'revs': all_reviews,
        'pics': pics,
    }
    return render(request, 'movieapp/details1.html', context)

@csrf_exempt
def catalog_grid(request):
    get_movies = movie.objects.all()
    cats = Category.objects.all()
    get_rate = rate.objects.all()
    get_year = year.objects.all()

    if request.method == 'POST':
        gen = request.POST.get('check')
        yearr = request.POST.get('year')

        check_genre = Category.objects.filter(cat=gen)
        fin = None

        # FILTER FOR GENRE AND DATE
        if gen:

            if check_genre:
                fin = Category.objects.get(cat=gen)

            genre_1 = movie.objects.filter(genre1=fin)
            genre_2 = movie.objects.filter(genre2=fin)

            if genre_1:
                if yearr:
                    return_result = movie.objects.filter(genre1=fin, year_range=yearr)
                    
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog1.html', context)
                else:
                    return_result = movie.objects.filter(genre1=fin)
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog1.html', context)  

            elif genre_2:
                if yearr:
                    return_result = movie.objects.filter(genre2=fin, year_range=yearr)
                    
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog1.html', context)
                else:
                    return_result = movie.objects.filter(genre2=fin)
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                        # return redirect('cat1')   
                    return render(request, 'movieapp/catalog1.html', context)
              
        if yearr:
            get_movies_by_year = movie.objects.filter(year_range=yearr)
            context = {
                'movies': get_movies_by_year,
                'category': cats,
                'rate': get_rate,
                'year': get_year
            }
                        # return redirect('cat1')   
            return render(request, 'movieapp/catalog1.html', context)
   
    context = {
        'movies': get_movies,
        'category': cats,
        'rate': get_rate,
        'year': get_year
    }
    return render(request, 'movieapp/catalog1.html', context)

def catalog_list(request):
    get_movies = movie.objects.all()
    cats = Category.objects.all()
    get_rate = rate.objects.all()
    get_year = year.objects.all()

    if request.method == 'POST':
        gen = request.POST.get('check')
        yearr = request.POST.get('year')

        check_genre = Category.objects.filter(cat=gen)
        fin = None

        # FILTER FOR GENRE AND DATE
        if gen:

            if check_genre:
                fin = Category.objects.get(cat=gen)

            genre_1 = movie.objects.filter(genre1=fin)
            genre_2 = movie.objects.filter(genre2=fin)

            if genre_1:
                if yearr:
                    return_result = movie.objects.filter(genre1=fin, year_range=yearr)
                    
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog2.html', context)
                else:
                    return_result = movie.objects.filter(genre1=fin)
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog2.html', context)  

            elif genre_2:
                if yearr:
                    return_result = movie.objects.filter(genre2=fin, year_range=yearr)
                    
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog2.html', context)
                else:
                    return_result = movie.objects.filter(genre2=fin)
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                        # return redirect('cat1')   
                    return render(request, 'movieapp/catalog2.html', context)
              
        if yearr:
            get_movies_by_year = movie.objects.filter(year_range=yearr)
            context = {
                'movies': get_movies_by_year,
                'category': cats,
                'rate': get_rate,
                'year': get_year
            }
                        # return redirect('cat1')   
            return render(request, 'movieapp/catalog2.html', context)

    context = {
        'movies': get_movies ,
        'category': cats,
        'rate': get_rate,
        'year': get_year
    }
    return render(request, 'movieapp/catalog2.html', context)

def Series(request):
    get_movies = series.objects.all()
    cats = Category.objects.all()
    get_rate = rate.objects.all()
    get_year = year.objects.all()

    if request.method == 'POST':
        gen = request.POST.get('check')
        yearr = request.POST.get('year')

        check_genre = Category.objects.filter(cat=gen)
        fin = None

          # FILTER FOR GENRE AND DATE
        if gen:

            if check_genre:
                fin = Category.objects.get(cat=gen)

            genre_1 = series.objects.filter(genre1=fin)
            genre_2 = series.objects.filter(genre2=fin)

            
            if genre_1:
                if yearr:
                    return_result = series.objects.filter(genre1=fin, year_range=yearr)
                    
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog2.html', context)
                else:
                    return_result = series.objects.filter(genre1=fin)
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog2.html', context)  

            elif genre_2:
                if yearr:
                    return_result = series.objects.filter(genre2=fin, year_range=yearr)
                    
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                    return render(request, 'movieapp/catalog2.html', context)
                else:
                    return_result = series.objects.filter(genre2=fin)
                    context = {
                        'movies': return_result,
                        'category': cats,
                        'rate': get_rate,
                        'year': get_year
                    }
                        # return redirect('cat1')   
                    return render(request, 'movieapp/catalog2.html', context)

        if yearr:
            get_movies_by_year = series.objects.filter(year_range=yearr)
            context = {
                'movies': get_movies_by_year,
                'category': cats,
                'rate': get_rate,
                'year': get_year
            }
                        # return redirect('cat1')   
            return render(request, 'movieapp/series.html', context)

    context = {
        'movies': get_movies ,
        'category': cats,
        'rate': get_rate,
        'year': get_year
    }
    return render(request, 'movieapp/series.html', context)

def pricing(request):
    return render(request, 'movieapp/pricing.html', {})

def faq(request):
    return render(request, 'movieapp/faq.html', {})

def about(request):
    return render(request, 'movieapp/about.html', {})

@login_required
def profile(request):
    my_user = User.objects.get(username=request.user)
    all_movies = movie.objects.all()
    all_series = series.objects.all()
    final = 0
    for i in all_movies:
        final+=1
    for j in all_series:
        final+=1
    # update profile
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
        confirm = request.POST.get('confirm')

        if oldpass:
            auth_user = authenticate(username=request.user.username,  password=oldpass)
            if auth_user is not None:
                if newpass == confirm:
                    my_user.set_password(confirm)
                    my_user.save()
                    logout(request)
                    return HttpResponse( 'Password updated successfully!. You will be redirected to the login page in a few seconds')
                else:
                    return HttpResponse('New & confirm password do not match!')
            else:
                return HttpResponse('Wrong details or user does not exist!')

        if username:
            my_user.username = username
            my_user.save()
            
        if email:
            my_user.email = email
            my_user.save()
            
        if name:
            fname = name.split()[0]
            lname = name.split()[1]
            my_user.first_name = fname
            my_user.last_name = lname
            my_user.save()
            
        return HttpResponse('Profile successfully updated')

    #movie & series comments
    get_comments_by_user = comment.objects.filter(name=request.user)
    get_series_comments_by_user = episode_comment.objects.filter(name=request.user)
    number_of_comments = 0
    for i in get_comments_by_user:
        number_of_comments+=1
    for i in get_series_comments_by_user:
        number_of_comments+=1

    #movie and series reviews
    number_of_reviews = 0
    get_reviews_by_user = reviewss.objects.filter(name=request.user)
    get_episode_reviews_by_user = episode_comment.objects.filter(name=request.user)
    for i in get_reviews_by_user:
        number_of_reviews+=1
    for i in get_episode_reviews_by_user:
        number_of_reviews+=1

    #get latest reviews
    get_reviews = reviewss.objects.filter(name=request.user)
    episode_review = er.objects.all().order_by('-date')[:5]


    #order movies by clicks
    for_you = series.objects.all().order_by('-clicks')[:4]
    for_you_movie = movie.objects.all().order_by('-clicks')[:4]

    context = {
        'num_comment': number_of_comments,
        'num_review': number_of_reviews,
        'revs': get_reviews,
        'for_you_series': for_you,
        'for_you_movie': for_you_movie,
        'episode_review': episode_review,
        'num_con': final,
    }
    return render(request, 'movieapp/profile.html', context)

def reset_password(request):
    myuser = User.objects.get(username=request.user)
    if request.method == 'POST':
        oldpass = request.POST['oldpass']
        newpass = request.POST['newpass']
        confirm = request.POST['confirmpass']

        auth_user = authenticate(username=request.user, password=oldpass)
        if auth_user is not None:
            if newpass == confirm:
                myuser.set_password(confirm)
                myuser.save()
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('profile')
        else:
            messages.error(request, 'You entered a wrong password')
            return redirect('profile')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        uname = request.POST['username']
        pass1 = request.POST['pass'] 
        
        my_user = authenticate(username=uname, password=pass1)
        if my_user is not None:
            get_profile = Profile.objects.get(user=my_user)
            if get_profile.verified  == False:
                messages.error(request, 'Your account has been temporarily banned due to misconduct.')
                return redirect('login')
            login(request, my_user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid password')
            return redirect('login')   
    
    return render(request, 'movieapp/signin.html', {})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST['name']
        user_name = request.POST['uname']
        email = request.POST['email']
        pass1 = request.POST['pass']

        if len(pass1) < 8:
            messages.error(request, 'Password is too short.')
            return redirect('register')

        check_username = User.objects.filter(username=name)
        if check_username:
            messages.error(request, 'Username already exists.')
            return redirect('register')

        check_email = User.objects.filter(email=email)
        if check_email:
            messages.error(request, 'Email already exists.')
            return redirect('register')

        try:
            first_name = name.split()[0]
            last_name = name.split()[1]

            new_user = User.objects.create_user(username=user_name, email=email, password=pass1)
            new_user.first_name=first_name
            new_user.last_name  = last_name
            new_user.save()

            new_profile = Profile(user=new_user, email=email, user_name=user_name)
            new_profile.save()

            messages.success(request, 'User successfully created. Login')
            return redirect('login')
        except:
            messages.success(request, 'Enter first & last names')
            return redirect('register')


    return render(request, 'movieapp/signup.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        check = User.objects.filter(email=email)
        if check:
            user=User.objects.get(email=email)
            email_templat_name = 'movieapp/email_template.html'

            c = {
                'username': user.username
            }
            emaill = render_to_string(email_templat_name, c)     

            email_mess = EmailMessage (
                'ProtonTv Password Reset',
                emaill,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_mess.fail_silently = True
            email_mess.content_subtype = 'html'
            email_mess.send()
            messages.success(request, 'We have sent you an email that will help you reset your password.')
            return redirect('reset-sent')
        else:
            messages.error(request, 'No user with that email exists')
            return redirect('fp')    

    return render(request, 'movieapp/forgot.html', {})

def password_reset_sent(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'movieapp/password-reset-sent.html', {})

def PasswordResedtView(request, name):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_view')
        if len(pass1) < 5:
            messages.error(request, 'Password cannot be less than 5 characters')
            return redirect('reset_view')

        user = User.objects.get(username=name)
        user.set_password(pass2)
        user.save()
        messages.success(request, 'Password successfully changed. Login now')
        return redirect('login')

    return render(request, 'movieapp/password-reset-form.html', {})


def privacy(request):
   
    return render(request, 'movieapp/privacy.html',{})

def contacts(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        sub = request.POST['subject']
        body  = request.POST['text']

        email_mess = EmailMessage (
                f'ProtonTv: {sub}',
                f'From: {name} \n \n Email: {email} \n \n Body: {body}',
                settings.EMAIL_HOST_USER,
                ['theprotonguy@yahoo.com']
            )
        email_mess.fail_silently = True
        email_mess.send()

        messages.success(request, 'Thank you for contacting us. We will reply shortly')
        return render(request, 'movieapp/contacts.html', {})
    
    return render(request, 'movieapp/contacts.html', {})
    

def NotFound(request, exception):
    return render(request, 'movieapp/404.html', {})

def series_detail(request, name):
    get_series = series.objects.get(name=name)
    get_season = season.objects.get(season_num='1', series_name=get_series)
    first_episode = episode.objects.get(series_name=get_series, season_val=get_season, episode_num='1')
    get_seasons = season.objects.filter(series_name=get_series)
    get_episodes = episode.objects.filter(series_name=get_series)

    # for i in get_seasons:
    #     get_episodes_for_display = episode.objects.filter(series_name=get_series, season_val=i)
    get_episodes_for_display = episode.objects.filter(series_name=get_series)

    fi = 0
    for i in get_episodes:
        fi+=1
    
    get_series.clicks +=1
    get_series.save()

    series_genre = get_series.genre1
    series_genre2 = get_series.genre2
    
    filtered_series = series.objects.filter(genre1=series_genre)
    filtered_series2 = series.objects.filter(genre2=series_genre2)

    filtered_series3 = series.objects.filter(genre1=series_genre2)
    filtered_series4 = series.objects.filter(genre2=series_genre2)

    pics = photos.objects.filter(series_name=get_series)

    context = {
        'series': get_series,
        'first_epi': first_episode,
        'season': get_seasons,
        'epi': fi,
        'episodes': get_episodes_for_display,
        'dis': filtered_series,
        'dis2': filtered_series2,
        'dis3': filtered_series3,
        'dis4': filtered_series4,
        'pic': pics
    }
    return render(request, 'movieapp/details2.html', context)

def series_detail_epi(request, name, seasons ,epi):
    get_series = series.objects.get(name=name)
    get_season = season.objects.get(season_num='1', series_name=get_series)
    first_episode = episode.objects.get(series_name=get_series, season_val=get_season, episode_num='1')
    get_seasons = season.objects.filter(series_name=get_series)
    get_episodes = episode.objects.filter(series_name=get_series)

    get_episodes_for_display = episode.objects.filter(series_name=get_series)

    get_series_for_episode = series.objects.get(name=name)


    part_se = episode.objects.get(series_name=get_series_for_episode, title=epi)
    epis = episode.objects.get(title=epi)

    if request.method == 'POST':
        if request.user.is_authenticated:
            get_profile = Profile.objects.get(user=request.user)
            com = request.POST.get('text')
            rev = request.POST.get('review')
            msg = request.POST.get('msg')
            rate = request.POST.get('rate')

            if rev:
                new_epi_review = er(name=request.user, body=msg, title=rev, rate=rate)
                new_epi_review.series_name = get_series_for_episode
                new_epi_review.episode = episode.objects.get(title=epi, series_name=get_series_for_episode)
                new_epi_review.save()
                get_profile.reviews +=1
                get_profile.save()
            elif com:
                new_epi_comment = episode_comment(name=request.user, body=com)
                new_epi_comment.series_name = get_series_for_episode
                new_epi_comment.episode = episode.objects.get(title=epi, series_name=get_series_for_episode)
                new_epi_comment.save()
                get_profile.comments +=1
                get_profile.save()
        else:
            messages.error(request, 'Please signin to post a comment or review')
            return redirect('series-detail-epi', name=name, seasons=seasons, epi=epi)

    
    get_episode_comments = episode_comment.objects.filter(episode = epis, series_name=get_series_for_episode)
    get_episode_reviews = er.objects.filter(episode = epis, series_name=get_series_for_episode)

    fi = 0
    for i in get_episodes:
        fi+=1

    series_genre = get_series.genre1
    
    series_genre2 = get_series.genre2
   
    filtered_series = series.objects.filter(genre1=series_genre)
    filtered_series2 = series.objects.filter(genre2=series_genre)
  

    filtered_series3 = series.objects.filter(genre1=series_genre2)
    filtered_series4 = series.objects.filter(genre2=series_genre2)


    pics = photos.objects.filter(series_name=get_series)

    context = {
        'series': get_series,
        'first_epi': first_episode,
        'season': get_seasons,
        'epi': fi,
        'episodes': get_episodes_for_display,
        'se': part_se,
        'coms': get_episode_comments,
        'revs': get_episode_reviews,
        'dis': filtered_series,
        'dis2': filtered_series2,
        'dis3': filtered_series3,
        'dis4': filtered_series4,
        'pic': pics,
    }
    return render(request, 'movieapp/epi.html', context)

