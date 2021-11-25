from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Review
from .forms import ReviewForm, ReviewCommentForm
from movies.models import Movie
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@require_GET
def index(request):
    reviews = Review.objects.all()
    paginator = Paginator(reviews, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews': page_obj,
    }

    return render(request, 'community/index.html', context)

@require_http_methods(['GET', 'POST'])
@login_required
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)

    else:
        form = ReviewForm()

    context = {
        'form': form
    }
    return render(request, 'community/create.html', context)


@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.reviewcomment_set.all()
    comment_form = ReviewCommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments
    }

    return render(request, 'community/detail.html', context)


@require_http_methods(['GET', 'POST'])
@login_required
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.user != review.user:
        return redirect('community:detail', review_pk)

    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)

    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review
    }

    return render(request, 'community/create.html', context)


@require_POST
def delete(request, review_pk):
    if request.method == "POST":
        review = get_object_or_404(Review, pk=review_pk)
    
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    
    return redirect('community:detail', review_pk)



@require_POST
@login_required
def create_comment(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        comment_form = ReviewCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            cnt= len(review.reviewcomment_set.all())

            context = {
                'username': request.user.username,
                'content': comment.content,
                'cnt': cnt
            }
            return JsonResponse(context)
        return redirect('community:detail', review.pk)
    return redirect('accounts:login')


@require_POST
@login_required
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            liked = False

        else:
            review.like_users.add(user)
            liked = True

        context = {
            'liked': liked,
            'count': review.like_users.count()
        }
        return JsonResponse(context)
    return redirect('accounts:login')


def search(request):
    context = dict()
    free_reviews = Review.objects.all()
    review = request.POST.get('review', "")

    if review:
        free_reviews = free_reviews.filter(title__icontains=review)
        context['free_reviews'] = free_reviews
        context['review'] = review
        return render(request, 'community/search.html', context)

    else:
        return render(request, 'community/search.html')



def search_movie(request):
    free_movies = Movie.objects.all()
    movie = request.GET.get('movie')
    
    if movie:
        free_movies = free_movies.filter(title__icontains=movie)
        selected = []

        for free_movie in free_movies:
            selected.append(model_to_dict(free_movie, fields=['title', 'poster_path']))

    return JsonResponse({'status': 200, 'data': selected})