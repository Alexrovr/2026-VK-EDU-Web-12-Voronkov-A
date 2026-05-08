from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user and username and '@' in username:
            try:
                email_user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                email_user = None
            if email_user:
                user = authenticate(username=email_user.username, password=password)

        if not user:
            raise forms.ValidationError("Неверный логин или пароль")
        self.user_cache = user
        return cleaned_data

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False, label="Аватар")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="О себе")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_repeat_password(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('repeat_password')
        if p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")
        return p2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        Profile.objects.get_or_create(user=user)
        return user

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Новый пароль')

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
