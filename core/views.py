from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile

def login_view(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def profile(request, user_id):
    user_data = get_object_or_404(User.objects.select_related('profile'), pk=user_id)
    return render(request, 'profile.html', {'user_profile': user_data})
