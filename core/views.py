from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from core.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import update_session_auth_hash
from core.forms import LoginForm, SignupForm, UserUpdateForm, ProfileUpdateForm

def login(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.user_cache)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        referer = request.META.get('HTTP_REFERER')
        if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()}):
            return redirect(referer)
        return redirect('index')
    return redirect('index')

def profile(request, user_id):
    user_data = get_object_or_404(User.objects.select_related('profile'), pk=user_id)
    return render(request, 'profile.html', {'user_profile': user_data})

@login_required
def settings(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            update_session_auth_hash(request, user)
            return redirect('settings')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'settings.html', context)
