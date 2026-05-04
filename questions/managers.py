from django.db import models
from django.db.models import Count

class QuestionManager(models.Manager):
    def get_new(self):
        return self.select_related('author', 'author__profile') \
        .prefetch_related('tags') \
        .annotate(answers_cnt=Count('answers')) \
        .filter(is_active=True) \
        .order_by('-updated_at')

    def get_hot(self):
        return self.select_related('author', 'author__profile') \
        .prefetch_related('tags') \
        .annotate(answers_cnt=Count('answers')) \
        .filter(rating__gte=1) \
        .filter(is_active=True) \
        .order_by('-rating')

    def get_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name) \
        .select_related('author', 'author__profile') \
        .prefetch_related('tags') \
        .annotate(answers_cnt=Count('answers')) \
        .filter(is_active=True) \
        .order_by('-updated_at')
