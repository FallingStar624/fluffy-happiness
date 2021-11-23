from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
from movies.models import CheckTime
from community.models import Review
from django.http.response import JsonResponse

# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile', request.user.username)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login') # 회원가입 완료시 로그인 페이지로 이동
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }        
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile', request.user.username)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:profile', request.user.username) # 홈화면으로 가도록 처리 필요
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

@login_required
def profile(request, username):
    profile_host = get_object_or_404(get_user_model(), username=username)
    host_movies = CheckTime.objects.filter(user_id=profile_host.pk)
    host_reviews = Review.objects.filter(user_id=profile_host.pk)
    context = {
        'profile_host': profile_host,
        'host_movies': host_movies,
        'host_reviews': host_reviews,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        profile_host = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if profile_host != user:
            if profile_host.followers.filter(pk=user.pk).exists():
                profile_host.followers.remove(user)
            else:
                profile_host.followers.add(user)
    return redirect('accounts:profile', profile_host.username)

