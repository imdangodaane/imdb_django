from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import make_password, is_password_usable
from django.core import serializers
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm, MovieForm, ActorForm, AwardForm
from .models import Actor, Movie, Award, MyUser, CustomUser
from .admin import CustomUserCreationForm
import json

# Create your views here.
def index(request):
    return render(request, 'imdb/index.html', context=None)

def login(request):
    try:
        next_page = request.GET['next']
    except KeyError:
        next_page = '/imdb/'
    if request.method == 'POST':
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     request.session['member_id'] = user.id
        #     return HttpResponseRedirect('/imdb/users/')
        # else:
        #     return HttpResponse("Invalid Login.")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                # request.session['member_id'] = user.id
                return HttpResponseRedirect(next_page)
            else:
                error_msg = 'There was an error!'
                return render(request, "imdb/login.html", {'form': form})
    else:
        form = LoginForm()
    return render(request, 'imdb/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/imdb/')

@login_required
def users(request):
    users = User.objects.all()
    users_json = list(users.values())
    return JsonResponse(users_json, safe=False, json_dumps_params={'indent': 4})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # data = form.save(commit=False)
            # data.password_confirm = ""
            # data.save()
            form.save()
            return render(request, 'imdb/signup_success.html')
    else:
        form = SignupForm()
    return render(request, 'imdb/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'imdb/signup_success.html')

@login_required
def movies(request):
    movies = Movie.objects.all()
    movies_json = list(movies.values())
    return JsonResponse(movies_json, safe=False, json_dumps_params={'indent': 4})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/movies/')
    else:
        form = MovieForm()
    return render(request, 'imdb/movies.html', {'form': form})

@login_required
def actors(request):
    actors = Actor.objects.all()
    actors_json = list(actors.values())
    return JsonResponse(actors_json, safe=False, json_dumps_params={'indent': 4})

@login_required
def add_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/actors/')
    else:
        form = ActorForm()
    return render(request, 'imdb/actors.html', {'form': form})

@login_required
def awards(request):
    awards = Award.objects.all()
    awards_json = list(awards.values())
    return JsonResponse(awards_json, safe=False, json_dumps_params={'indent': 4})

@login_required
def add_award(request):
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/awards/')
    else:
        form = AwardForm()
    return render(request, 'imdb/awards.html', {'form': form})