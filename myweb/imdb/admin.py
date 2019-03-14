from django import forms
from django.contrib import admin
from imdb.models import Movie, Actor, Award, Comment

# Register your models here.

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Award)
admin.site.register(Comment)