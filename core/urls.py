from django.urls import path
from core import views
from core.views import LoginView, SignupView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
