from django.urls import path
from questions import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('api/question/<int:question_id>/edit/', views.QuestionUpdateAPI.as_view(), name='api_question_edit'),
    path('api/question/<int:question_id>/answer/', views.AnswerCreateAPI.as_view(), name='api_answer_create'),
    path('api/answer/<int:answer_id>/edit/', views.AnswerUpdateAPI.as_view(), name='api_answer_edit'),
    path('ask/', views.AskView.as_view(), name='ask'),
]
