from django.urls import path, include
from . import views

app_name = 'imdb'

urlpatterns = [
    # Index
    path('', views.index, name='index'),
    
    # Authentication URLS
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),

    # Movie URLS
    path('movies/', views.movies, name='movies'),
    path('movies/add/', views.add_movie, name='addmovie'),
    path('movies/detail/<int:pk>/', views.movie_detail, name="moviedetail"),

    # Actor URLS
    path('actors/', views.actors, name='actors'),
    path('actors/add/', views.add_actor, name='addactor'),
    path('actors/detail/<int:pk>/', views.actor_detail, name="actordetail"),

    # Award URLS
    path('awards/', views.awards, name='awards'),
    path('awards/add/', views.add_award, name='addaward'),
    path('awards/detail/<int:pk>/', views.award_detail, name="awarddetail"),

    # User URLS
    path('users/', views.users, name='users'),
]