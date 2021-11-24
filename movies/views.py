import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import Movie, Genre, MovieComment
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from .forms import MovieCommentForm
from community.models import Review
from django.contrib.auth import get_user




# Create your views here.
def home(request):
    user = get_user(request)
    watch_movie = user.watch_movies.all().order_by('-checktime').first()
    
    if watch_movie == None:
        movies = []
    else:
        movies = watch_movie.recommend.all()

    context = {
        'movies': movies,
    }

    return render(request, 'movies/home.html', context)



def index(request):
    genres = Genre.objects.all()

    context = {
        'genres': genres,
    }

    return render(request, 'movies/index.html', context)



def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comments = movie.moviecomment_set.all()
    comment_form = MovieCommentForm()

    context = {
        'movie': movie,
        'movie_comments': movie_comments,
        'comment_form': comment_form
    }

    return render(request, 'movies/detail.html', context)




def api_movie(request):
    movies = Movie.objects.all()

    data_movie = serializers.serialize('json', movies)

    return HttpResponse(data_movie, content_type='application/json')



def api_genre(request):
    genres = Genre.objects.all()

    data_genre = serializers.serialize('json', genres)

    return HttpResponse(data_genre, content_type='application/json')


def search_movie(request):
    free_movies = Movie.objects.all()
    movie = request.GET.get('movie')

    if movie:
        free_movies = free_movies.filter(title__icontains=movie)
        selected = []

        for free_movie in free_movies:
            selected.append(model_to_dict(free_movie, fields=['title', 'poster_path', 'id']))
            

        # context = serializers.serialize('json', selected)
    return JsonResponse({'status': 200, 'data': selected})






def create_moviecomment(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        comment_form = MovieCommentForm(request.POST)
        
        if comment_form.is_valid():
            movie_comment = comment_form.save(commit=False)
            movie_comment.movie = movie
            movie_comment.user = request.user
            movie_comment.save()
            reviewcnt = len(movie.moviecomment_set.all())
        
            context = {
                'username': request.user.username,
                'moviecontent': movie_comment.content,
                'reviewcnt': reviewcnt
            }
            return JsonResponse(context)
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')



def watch(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user

        if movie.watch_users.filter(pk=user.pk).exists():
            movie.watch_users.remove(user)
            watched = False
        else:
            movie.watch_users.add(user)
            watched = True

        context = {
            'watched': watched,
            'count': movie.watch_users.count()
        }
        return JsonResponse(context)
    return redirect('accounts:login')

