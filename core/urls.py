from django.urls import path
from core import views
from core.views import LoginView, SignupView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]
