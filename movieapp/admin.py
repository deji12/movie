from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.movie)
admin.site.register(models.comment)
admin.site.register(models.reviewss)
admin.site.register(models.Category)
admin.site.register(models.rate)
admin.site.register(models.year)
admin.site.register(models.series)
admin.site.register(models.episode_comment)
admin.site.register(models.episode_review)
admin.site.register(models.season)
admin.site.register(models.episode)
admin.site.register(models.photos)