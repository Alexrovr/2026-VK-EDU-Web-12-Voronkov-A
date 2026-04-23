from django.contrib.auth.models import User
from django.db.models import Count
from questions.models import Tag

def sidebar_data(request):
    top_users = User.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:5]
    popular_tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]
    return {'top_users': top_users, 'popular_tags': popular_tags}
