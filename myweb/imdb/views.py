from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import LoginForm, SignupForm, MovieForm, ActorForm, AwardForm
from .models import Actor, Movie, Award
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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
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
            form.save()
            return render(request, 'imdb/signup_success.html')
    else:
        form = SignupForm()
    return render(request, 'imdb/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'imdb/signup_success.html')

@login_required
def movies(request):
    movies = list(Movie.objects.all().order_by('title'))
    recent_added = list(Movie.objects.all().order_by('-id'))[:3]
    return render(request, 'imdb/movies.html', {'movies': movies, 'recent_added': recent_added})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            new_movie = form.save(commit=False)
            new_movie.save()
            form.save_m2m()
            return HttpResponseRedirect('/imdb/movies/')
    else:
        form = MovieForm()
    return render(request, 'imdb/add_movie.html', {'form': form})

@login_required
def movie_detail(request, pk):
    obj = get_object_or_404(Movie, pk=pk)
    return render(request, 'imdb/movie_detail.html', {'obj': obj,})

@login_required
def actors(request):
    actors = list(Actor.objects.all().order_by('first_name'))
    recent_added = list(Actor.objects.all().order_by('-id'))[:3]
    return render(request, 'imdb/actors.html', {'actors': actors, 'recent_added': recent_added})

@login_required
def add_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/actors/')
    else:
        form = ActorForm()
    return render(request, 'imdb/add_actor.html', {'form': form})

@login_required
def actor_detail(request, pk):
    obj = get_object_or_404(Actor, pk=pk)
    return render(request, 'imdb/actor_detail.html', {'obj': obj,})

@login_required
def awards(request):
    awards = list(Award.objects.all().order_by('name'))
    movie_awards = list(Award.objects.filter(kind__iexact='Movie'))
    actor_awards = list(Award.objects.filter(kind__iexact='Actor'))
    recent_added = list(Award.objects.all().order_by('-id'))[:3]
    return render(request, 'imdb/awards.html', {'awards': awards,
                                                'recent_added': recent_added,
                                                'movie_awards': movie_awards,
                                                'actor_awards': actor_awards,})

@login_required
def add_award(request):
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/awards/')
    else:
        form = AwardForm()
    return render(request, 'imdb/add_award.html', {'form': form})

@login_required
def award_detail(request, pk):
    obj = get_object_or_404(Award, pk=pk)
    return render(request, 'imdb/award_detail.html', {'obj': obj,})