from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('search-movie/', views.search_movie, name='search_movie'),
    path('api-movie/', views.api_movie),
    path('api-genre/', views.api_genre),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/comments/create/', views.create_moviecomment, name='create_moviecomment'),
    path('<int:movie_pk>/watch/', views.watch, name='watch'),
]
