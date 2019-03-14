from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import LoginForm, SignupForm, MovieForm, ActorForm, AwardCreateForm, AwardAssignForm, CommentForm
from .models import Actor, Movie, Award, Comment
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils import timezone
import json

# Create your views here.

#=====================================COMMENT=====================================#
def comment_update(request, pk):
    if request.method == 'POST':
        comment_update = request.POST.get('comment_update')
        try:
            cmt = Comment.objects.get(pk=pk)
            cmt.content = comment_update
            cmt.last_edit = timezone.now()
            cmt.save()
            return_url = '/imdb/' + str(cmt.target_kind).lower() + 's/detail/' + str(cmt.target_id)
            return HttpResponseRedirect(return_url)
        except Comment.DoesNotExist:
            pass
    else:
        return HttpResponseRedirect('/imdb/')

def comment_delete(request, pk):
    if request.method == 'POST':
        current_movie_id = request.POST.get('current_movie_id')
        try:
            cmt = Comment.objects.get(pk=pk)
            return_url = '/imdb/' + str(cmt.target_kind).lower() + 's/detail/' + str(cmt.target_id)
            cmt.delete()
            return HttpResponseRedirect(return_url)
        except Comment.DoesNotExist:
            pass
    else:
        return HttpResponseRedirect('/imdb/movies/detail/')

#=====================================AUTHENTICATION=====================================#
def index(request):
    return render(request, 'imdb/index.html', context=None)

@login_required
def users(request):
    users = User.objects.all()
    users_json = list(users.values())
    return JsonResponse(users_json, safe=False, json_dumps_params={'indent': 4})

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

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'imdb/signup_success.html')
        else:
            return render(request, 'imdb/signup.html', {'form': form,})
    else:
        form = SignupForm()
    return render(request, 'imdb/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'imdb/signup_success.html')


#=====================================MOVIE=====================================#

@login_required
def update_movie(request, pk):
    if request.method == "POST":
        try:
            old_obj = Movie.objects.get(pk=pk)
            new_form = MovieForm(request.POST, request.FILES, instance=old_obj)
        except Movie.DoesNotExist:
            new_form = MovieForm(request.POST)
        if new_form.is_valid():
            new_form.save()
            return HttpResponseRedirect('/imdb/movies/detail/' + str(pk))
        else:
            return HttpResponseRedirect('/imdb/movies/')
    else:
        return HttpResponseRedirect('/imdb/movies/')


@login_required
def delete_movie(request, pk):
    if request.method == "POST":
        try:
            obj = Movie.objects.get(pk=pk)
            obj.delete()
        except Movie.DoesNotExist:
            pass
    return HttpResponseRedirect('/imdb/movies/')

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
    if request.method == 'POST':
        cmt_form = CommentForm(request.POST)
        if cmt_form.is_valid():
            cmt_data = cmt_form.save(commit=False)
            cmt_data.user = request.user
            cmt_data.target_kind = request.POST.get('kind')
            cmt_data.target_id = pk
            cmt_data.save()
            return_url = '/imdb/' + str(cmt_data.target_kind).lower() + 's/detail/' + str(cmt_data.target_id)
            return HttpResponseRedirect(return_url)
    else:
        obj = get_object_or_404(Movie, pk=pk)
        pre_form = MovieForm(obj.__dict__)
        cmt_form = CommentForm()
        load_comments = Comment.objects.filter(target_kind__iexact='movie', target_id__exact=obj.id).order_by('-created_time')
        return render(request, 'imdb/movie_detail.html', {'obj': obj, 
                                                          'cmt_form': cmt_form, 
                                                          'load_comments': load_comments,
                                                          'pre_form': pre_form,})

#=====================================ACTOR=====================================#
@login_required
def update_actor(request, pk):
    if request.method == "POST":
        try:
            old_obj = Actor.objects.get(pk=pk)
            new_form = ActorForm(request.POST, instance=old_obj)
        except Movie.DoesNotExist:
            new_form = ActorForm(request.POST)
        if new_form.is_valid():
            new_form.save()
            return HttpResponseRedirect('/imdb/actors/detail/' + str(pk))
        else:
            return HttpResponseRedirect('/imdb/actors/')
    else:
        return HttpResponseRedirect('/imdb/actors/')


@login_required
def delete_actor(request, pk):
    if request.method == "POST":
        try:
            obj = Actor.objects.get(pk=pk)
            obj.delete()
        except Actor.DoesNotExist:
            pass
    return HttpResponseRedirect('/imdb/actors/')
    
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
        print(form)
    return render(request, 'imdb/add_actor.html', {'form': form})

@login_required
def actor_detail(request, pk):
    if request.method == 'POST':
        cmt_form = CommentForm(request.POST)
        if cmt_form.is_valid():
            cmt_data = cmt_form.save(commit=False)
            cmt_data.user = request.user
            cmt_data.target_kind = request.POST.get('kind')
            cmt_data.target_id = pk
            cmt_data.save()
            return_url = '/imdb/' + str(cmt_data.target_kind).lower() + 's/detail/' + str(cmt_data.target_id)
            return HttpResponseRedirect(return_url)
    else:
        obj = get_object_or_404(Actor, pk=pk)
        pre_form = ActorForm(obj.__dict__)
        cmt_form = CommentForm()
        load_comments = Comment.objects.filter(target_kind__iexact='actor', target_id__exact=obj.id).order_by('-created_time')
        return render(request, 'imdb/actor_detail.html', {'obj': obj, 
                                                          'cmt_form': cmt_form, 
                                                          'load_comments': load_comments,
                                                          'pre_form': pre_form,})

#=====================================AWARD=====================================#
@login_required
def update_award(request, pk):
    if request.method == "POST":
        try:
            old_obj = Award.objects.get(pk=pk)
            new_form = AwardCreateForm(request.POST, instance=old_obj)
        except Award.DoesNotExist:
            new_form = AwardCreateForm(request.POST)
        if new_form.is_valid():
            new_form.save()
            return HttpResponseRedirect('/imdb/awards/detail/' + str(pk))
        else:
            return HttpResponseRedirect('/imdb/awards/')
    else:
        return HttpResponseRedirect('/imdb/awards/')

@login_required
def assign_award(request, pk):
    if request.method == "POST":
        try:
            old_obj = Award.objects.get(pk=pk)
            new_form = AwardAssignForm(request.POST, instance=old_obj)
        except Award.DoesNotExist:
            new_form = AwardAssignForm(request.POST)
        print(new_form)
        print(new_form.is_valid())
        if new_form.is_valid():
            new_form.save()
            return HttpResponseRedirect('/imdb/awards/detail/' + str(pk))
        else:
            return HttpResponseRedirect('/imdb/awards/')
    else:
        return HttpResponseRedirect('/imdb/awards/')


@login_required
def delete_award(request, pk):
    if request.method == "POST":
        try:
            obj = Award.objects.get(pk=pk)
            obj.delete()
        except Award.DoesNotExist:
            pass
    return HttpResponseRedirect('/imdb/awards/')

@login_required
def awards(request):
    awards = list(Award.objects.all().order_by('name'))
    movie_awards = list(Award.objects.filter(kind__iexact='Movie'))
    actor_awards = list(Award.objects.filter(kind__iexact='Actor'))
    recent_added = list(Award.objects.all().order_by('-id'))[:3]
    return render(request, 'imdb/awards.html', {'awards': awards,
                                                'recent_added': recent_added,
                                                'movie_awards': movie_awards,
                                                'actor_awards': actor_awards,
                                                })

@login_required
def add_award(request):
    if request.method == 'POST':
        form = AwardCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/imdb/awards/')
    else:
        form = AwardCreateForm()
    return render(request, 'imdb/add_award.html', {'form': form})

@login_required
def award_detail(request, pk):
    if request.method == 'POST':
        cmt_form = CommentForm(request.POST)
        if cmt_form.is_valid():
            cmt_data = cmt_form.save(commit=False)
            cmt_data.user = request.user
            cmt_data.target_kind = request.POST.get('kind')
            cmt_data.target_id = pk
            cmt_data.save()
            return_url = '/imdb/' + str(cmt_data.target_kind).lower() + 's/detail/' + str(cmt_data.target_id)
            return HttpResponseRedirect(return_url)
    else:
        obj = get_object_or_404(Award, pk=pk)
        pre_form = AwardCreateForm(obj.__dict__)
        assign_form = AwardAssignForm(obj.__dict__)
        cmt_form = CommentForm()
        load_comments = Comment.objects.filter(target_kind__iexact='award', target_id__exact=obj.id).order_by('-created_time')
        return render(request, 'imdb/award_detail.html', {'obj': obj, 
                                                          'cmt_form': cmt_form, 
                                                          'load_comments': load_comments,
                                                          'pre_form': pre_form,
                                                          'assign_form': assign_form})