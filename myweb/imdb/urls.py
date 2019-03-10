from django.urls import path, include
from . import views

app_name = 'imdb'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('movies/', views.movies, name='movies'),
    path('movies/add/', views.add_movie, name='addmovie'),
    # path('movies/detail/', views.movies_detail, name='moviesdetail'),
    path('actors/', views.actors, name='actors'),
    path('actors/add/', views.add_actor, name='addactor'),
    # path('actors/detail/', views.actors_detail, name='actorsdetail'),
    path('awards/', views.awards, name='awards'),
    path('awards/add/', views.add_award, name='addaward'),
    # path('awards/detail/', views.awards_detail, name='awardsdetail'),
    path('users/', views.users, name='users'),

]