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
    path('movies/detail/<int:pk>/update/', views.update_movie, name="updatemovie"),
    path('movies/detail/<int:pk>/delete/', views.delete_movie, name="deletemovie"),


    # Actor URLS
    path('actors/', views.actors, name='actors'),
    path('actors/add/', views.add_actor, name='addactor'),
    path('actors/detail/<int:pk>/', views.actor_detail, name="actordetail"),
    path('actors/detail/<int:pk>/update/', views.update_actor, name="updateactor"),
    path('actors/detail/<int:pk>/delete/', views.delete_actor, name="deleteactor"),

    # Award URLS
    path('awards/', views.awards, name='awards'),
    path('awards/add/', views.add_award, name='addaward'),
    path('awards/detail/<int:pk>/', views.award_detail, name="awarddetail"),
    path('awards/detail/<int:pk>/update/', views.update_award, name="updateaward"),
    path('awards/detail/<int:pk>/assign', views.assign_award, name='assignaward'),
    path('awards/detail/<int:pk>/delete/', views.delete_award, name="deleteaward"),

    # User URLS
    path('users/', views.users, name='users'),

    # Comment URLS
    path('comment/<int:pk>', views.movie_detail, name="addcomment"),
    path('comment/<int:pk>/', views.comment_update, name='comment-update'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment-delete'),
]