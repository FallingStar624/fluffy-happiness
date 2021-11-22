import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import Movie, Genre, MovieComment
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from .forms import MovieCommentForm




# Create your views here.
def home(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies
    }

    return render(request, 'movies/_grid.html', context)



def index(request):
    genres = Genre.objects.all()
    # movies = Movie.objects.all()
    # paginator = Paginator(movies, 10)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     data = serializers.serialize('json', page_obj)
    #     return HttpResponse(data, content_type='application/json')

    # else:
    context = {
        'genres': genres,
        # 'movies': page_obj
    }

    return render(request, 'movies/index.html', context)



def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    context = {
        'movie': movie
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
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment_form = MovieCommentForm(request.POST)
    
    if comment_form.is_valid():
        movie_comment = comment_form.save(commit=False)
        movie_comment.movie = movie
        movie_comment.user = request.user
        movie_comment.save()
        return redirect('movies:detail', movie.pk)
    
    else:
        comment_form = MovieCommentForm()
    
    context = {
        'comment_form': comment_form,
        'movie': movie,
        'movie_comments': movie.moviecomment_set.all(),
    }
    return render(request, 'movies/detail.html', context)



def like(request, review_pk):
    pass
    # if request.user.is_authenticated:
    #     review = get_object_or_404(Movie, pk=review_pk)
    #     user = request.user

    #     if review.like_users.filter(pk=user.pk).exists():
    #         review.like_users.remove(user)
    #         liked = False
    #     else:
    #         review.like_users.add(user)
    #         liked = True

    #     context = {
    #         'liked': liked,
    #         'count': review.like_users.count()
    #     }
    #     return JsonResponse(context)
    # return redirect('accounts:login')
