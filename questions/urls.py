from django.urls import path
from questions import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask/', views.AskView.as_view(), name='ask'),
]
