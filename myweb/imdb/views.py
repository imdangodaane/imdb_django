from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import make_password, is_password_usable
from django.core import serializers
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, MovieForm, ActorForm, AwardForm
from .models import Actor, Movie, Award, MyUser
import json

# Create your views here.
def index(request):
    return render(request, 'imdb/index.html', context=None)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(request.session.items())
            return HttpResponseRedirect('/imdb/users/')
        else:
            return HttpResponse("Invalid Login.")
    else:
        form = LoginForm()
    return render(request, 'imdb/login.html', {'form': form})

def users(request):
    users = MyUser.objects.all()
    users_json = list(users.values())
    return JsonResponse(users_json, safe=False, json_dumps_params={'indent': 4})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.password_confirm = ""
            data.save()
            return render(request, 'imdb/signup_success.html')
    else:
        form = SignupForm()
    return render(request, 'imdb/signup.html', {'form': form})

def movies(request):
    movies = Movie.objects.all()
    movies_json = list(movies.values())
    return JsonResponse(movies_json, safe=False, json_dumps_params={'indent': 4})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/movies/')
    else:
        form = MovieForm()
    return render(request, 'imdb/movies.html', {'form': form})

def actors(request):
    actors = Actor.objects.all()
    actors_json = list(actors.values())
    return JsonResponse(actors_json, safe=False, json_dumps_params={'indent': 4})

def add_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/actors/')
    else:
        form = ActorForm()
    return render(request, 'imdb/actors.html', {'form': form})

def awards(request):
    awards = Award.objects.all()
    awards_json = list(awards.values())
    return JsonResponse(awards_json, safe=False, json_dumps_params={'indent': 4})

def add_award(request):
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/awards/')
    else:
        form = AwardForm()
    return render(request, 'imdb/awards.html', {'form': form})