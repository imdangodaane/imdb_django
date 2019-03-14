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
    """Update edited comment in a specific page"""
    if request.method == 'POST':
        # Get the edited comment from request.POST object
        comment_update = request.POST.get('comment_update')
        try:
            # Get comment object by primary key (pk), update new content of comment then save
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
    """Delete a specific comment in a specific page"""
    if request.method == 'POST':
        try:
            # Get comment object by primary key then delete from database
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
    """Index view"""
    return render(request, 'imdb/index.html', context=None)


@login_required
def users(request):
    """User list view as json"""
    users = User.objects.all()
    users_json = list(users.values())
    return JsonResponse(users_json, safe=False, json_dumps_params={'indent': 4})


def login(request):
    """Login view"""
    # Try to get next page after login
    try:
        next_page = request.GET['next']
    except KeyError:
        next_page = '/imdb/'
    # Login Authentication
    if request.method == 'POST':
        # Get login form from template
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            # Authenticate user
            if user is not None and user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                error_msg = 'There was an error!'
                return render(request, "imdb/login.html", {'form': form})
    else:
        # Send login form to template
        form = LoginForm()
    return render(request, 'imdb/login.html', {'form': form})


def logout(request):
    """Logout view"""
    auth_logout(request)
    return HttpResponseRedirect('/imdb/')


def signup(request):
    """Signup view"""
    if request.method == 'POST':
        # Get signup form from template
        form = SignupForm(request.POST)
        if form.is_valid():
            # Valid form then save
            form.save()
            return render(request, 'imdb/signup_success.html')
        else:
            return render(request, 'imdb/signup.html', {'form': form,})
    else:
        # Send signup form to template
        form = SignupForm()
    return render(request, 'imdb/signup.html', {'form': form})


def signup_success(request):
    """Signup success view"""
    return render(request, 'imdb/signup_success.html')


#=====================================MOVIE=====================================#
@login_required
def update_movie(request, pk):
    """Update/edit movie view"""
    if request.method == "POST":
        try:
            # Get new form of movie from template and replace it to old object
            old_obj = Movie.objects.get(pk=pk)
            new_form = MovieForm(request.POST, request.FILES, instance=old_obj)
        except Movie.DoesNotExist:
            # If there's no old object, create new form movie
            new_form = MovieForm(request.POST)
        if new_form.is_valid():
            # Save to database
            new_form.save()
            return HttpResponseRedirect('/imdb/movies/detail/' + str(pk))
        else:
            return HttpResponseRedirect('/imdb/movies/')
    else:
        return HttpResponseRedirect('/imdb/movies/')


@login_required
def delete_movie(request, pk):
    """Delete movie view"""
    if request.method == "POST":
        try:
            # Try to get movie object by primary key then delete
            obj = Movie.objects.get(pk=pk)
            obj.delete()
        except Movie.DoesNotExist:
            pass
    return HttpResponseRedirect('/imdb/movies/')


@login_required
def movies(request):
    """Movie list view"""
    # Get all movie object
    movies = list(Movie.objects.all().order_by('title'))
    # Get 3 movie objects from database
    recent_added = list(Movie.objects.all().order_by('-id'))[:3]
    # Render all movie objects to template
    return render(request, 'imdb/movies.html', {'movies': movies, 'recent_added': recent_added})


@login_required
def add_movie(request):
    """Add movie view"""
    if request.method == 'POST':
        # Get new movie form from request object
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            # Valid form and then save
            new_movie = form.save(commit=False)
            new_movie.save()
            # Save many to many field need 2 steps as aboe
            form.save_m2m()
            return HttpResponseRedirect('/imdb/movies/')
    else:
         # Send new movie form to template
        form = MovieForm()
    return render(request, 'imdb/add_movie.html', {'form': form})


@login_required
def movie_detail(request, pk):
    """Movie detail view"""
    if request.method == 'POST':
        # Get comment form from request if there someone comment
        cmt_form = CommentForm(request.POST)
        if cmt_form.is_valid():
            # Valid comment form, add some related informations then save
            cmt_data = cmt_form.save(commit=False)
            cmt_data.user = request.user
            cmt_data.target_kind = request.POST.get('kind')
            cmt_data.target_id = pk
            cmt_data.save()
            return_url = '/imdb/' + str(cmt_data.target_kind).lower() + 's/detail/' + str(cmt_data.target_id)
            return HttpResponseRedirect(return_url)
    else:
        # Get movie object
        obj = get_object_or_404(Movie, pk=pk)
        # Get some form serving for edit/delete purpose
        # pre_form is previous form of object was save in database
        # send pre-form to template for editing purpose
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
    """Update actor view"""
    if request.method == "POST":
        try:
            # Replace old object as new form receive from template
            old_obj = Actor.objects.get(pk=pk)
            new_form = ActorForm(request.POST, instance=old_obj)
        except Movie.DoesNotExist:
            # If old object not exist, just get new form
            new_form = ActorForm(request.POST)
        if new_form.is_valid():
            # Valid form and save
            new_form.save()
            return HttpResponseRedirect('/imdb/actors/detail/' + str(pk))
        else:
            return HttpResponseRedirect('/imdb/actors/')
    else:
        return HttpResponseRedirect('/imdb/actors/')


@login_required
def delete_actor(request, pk):
    """Delete actor view"""
    if request.method == "POST":
        try:
            obj = Actor.objects.get(pk=pk)
            obj.delete()
        except Actor.DoesNotExist:
            pass
    return HttpResponseRedirect('/imdb/actors/')


@login_required
def actors(request):
    """Actor list view"""
    actors = list(Actor.objects.all().order_by('first_name'))
    recent_added = list(Actor.objects.all().order_by('-id'))[:3]
    return render(request, 'imdb/actors.html', {'actors': actors, 'recent_added': recent_added})


@login_required
def add_actor(request):
    """Add actor view"""
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
    """Actor detail view"""
    if request.method == 'POST':
        cmt_form = CommentForm(request.POST)
        if cmt_form.is_valid():
            # Get comment object, save related informations and save
            cmt_data = cmt_form.save(commit=False)
            cmt_data.user = request.user
            cmt_data.target_kind = request.POST.get('kind')
            cmt_data.target_id = pk
            cmt_data.save()
            return_url = '/imdb/' + str(cmt_data.target_kind).lower() + 's/detail/' + str(cmt_data.target_id)
            return HttpResponseRedirect(return_url)
    else:
        # Get some form serving for edit/delete purpose
        # pre_form is previous form of object was save in database
        # send pre-form to template for editing purpose
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
    """Update award view"""
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
    """Assign award view"""
    if request.method == "POST":
        try:
            # Get Award assign form from template
            old_obj = Award.objects.get(pk=pk)
            new_form = AwardAssignForm(request.POST, instance=old_obj)
        except Award.DoesNotExist:
            new_form = AwardAssignForm(request.POST)
        if new_form.is_valid():
            # Assign Award related informations and save
            data = new_form.save(commit=False)
            data.date_assign = timezone.now()
            data.save()
            new_form.save_m2m()
            return HttpResponseRedirect('/imdb/awards/detail/' + str(pk))
        else:
            return HttpResponseRedirect('/imdb/awards/')
    else:
        return HttpResponseRedirect('/imdb/awards/')


@login_required
def delete_award(request, pk):
    """Delete award view"""
    if request.method == "POST":
        try:
            obj = Award.objects.get(pk=pk)
            obj.delete()
        except Award.DoesNotExist:
            pass
    return HttpResponseRedirect('/imdb/awards/')


@login_required
def awards(request):
    """Award list view"""
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
    """Add award view"""
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
    """Award detail view"""
    if request.method == 'POST':
        # Get comment from user and save
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
        # Get some form serving for edit/delete purpose
        # pre_form/assign_form is previous form of object was save in database
        # send pre-form to template for editing purpose
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
