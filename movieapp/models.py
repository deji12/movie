from audioop import add
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    verified = models.BooleanField(default=True)
    pricing_plan = models.CharField(max_length=100, default='Free', null=True, blank=True)
    email = models.CharField(max_length=1000,  null=True, blank=True)
    user_name = models.CharField(max_length=1000, null=True, blank=True)
    comments = models.IntegerField(default=0, null=True, blank=True)
    reviews = models.IntegerField(default=0, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Category(models.Model):
    cat = models.CharField(max_length=1000)

    def __str__(self):
        return self.cat

class rate(models.Model):
    rate_value = models.CharField(max_length=1000)

class year(models.Model):
    year_value = models.CharField(max_length=200)

    def __str__(self):
        return self.year_value

class movie(models.Model):
    name = models.CharField(max_length=20000)
    info = models.TextField()
    video = models.CharField(max_length=10000, null=True, blank=True)
    thumbnail = models.FileField(upload_to='thumb/')
    age = models.CharField(default=13, max_length=20)
    cat = models.CharField(default='cartoon', max_length=200)
    premier = models.BooleanField(default=False)
    genre1 = models.ForeignKey(Category, related_name='category1', on_delete=models.CASCADE, null=True, blank=True)
    genre2 = models.ForeignKey(Category, related_name='category2', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    year_range = models.CharField(max_length=200, null=True, blank=True)
    new = models.BooleanField(default=False)
    duration = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    draft = models.BooleanField(default=False)
    date_added = models.DateField(auto_now_add=True, null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name

class comment(models.Model):
    movie = models.ForeignKey(movie, related_name='movie_comment', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.movie)

class reviewss(models.Model):
    movie = models.ForeignKey(movie, related_name='movie_review', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000)
    body = models.TextField()
    rate = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.movie)

# series

class series(models.Model):
    name = models.CharField(max_length=20000)
    info = models.TextField()
    thumbnail = models.FileField(upload_to='thumb/series/')
    age = models.CharField(default=13, max_length=20)
    genre1 = models.ForeignKey(Category, related_name='series_category1', on_delete=models.CASCADE, null=True, blank=True)
    genre2 = models.ForeignKey(Category, related_name='series_category2', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.CharField(max_length=100)
    new = models.BooleanField(default=False)
    premier = models.BooleanField(default=False)
    series_air_date = models.DateField(auto_now_add=True)
    year_range = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    draft = models.BooleanField(default=False)
    clicks = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.name)

class photos(models.Model):
    series_name = models.ForeignKey(series, on_delete=models.CASCADE, null=True, blank=True)
    movie_name = models.ForeignKey(movie, on_delete=models.CASCADE, null=True, blank=True)
    pic = models.FileField(upload_to='movie-photos')

    def __str__(self):
        return str(self.movie_name)

class season(models.Model):
    series_name = models.ForeignKey(series, related_name='season_val', on_delete=models.CASCADE)
    season_num = models.CharField(max_length=100)
    heading = models.CharField(max_length=100, blank=True, null=True)
    collapse = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return str(f'{self.series_name} | Season {self.season_num}')

class episode(models.Model):
    title = models.CharField(max_length=200, default='title')
    series_name = models.ForeignKey(series, related_name='season_epi', on_delete=models.CASCADE)
    season_val = models.ForeignKey(season, related_name='episode', on_delete=models.CASCADE)   
    episode_num = models.CharField(max_length=100, default='1') 
    video = models.CharField(max_length=10000, null=True, blank=True)
    duration = models.CharField(max_length=100)
    dou = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.season_val}')

class series_comment(models.Model):
    pass

class episode_comment(models.Model):
    episode = models.ForeignKey(episode, related_name='series_comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    series_name = models.ForeignKey(series, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.series_name)

class episode_review(models.Model):
    episode = models.ForeignKey(episode, related_name='series_reviews', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    series_name = models.ForeignKey(series, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=5000)
    body = models.TextField()
    rate = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.series_name)



