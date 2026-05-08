from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import LoginForm, SignupForm

def login(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.user_cache)
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                next_url = '/'
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

def profile(request, user_id):
    user_data = get_object_or_404(User.objects.select_related('profile'), pk=user_id)
    return render(request, 'profile.html', {'user_profile': user_data})

@login_required
def settings(request):
    user = User.objects.select_related('profile').get(pk=request.user.id)
    return render(request, 'settings.html', {'user': user})
