from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from core.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import update_session_auth_hash
from core.forms import LoginForm, SignupForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return reverse_lazy('index')

    def form_valid(self, form):
        auth.login(self.request, form.user_cache)
        return super().form_valid(form)

class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return super().form_valid(form)

@require_POST
def logout(request):
    auth.logout(request)
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
