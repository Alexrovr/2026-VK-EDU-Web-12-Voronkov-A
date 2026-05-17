from django.db import models
from django.db.models import Count, Prefetch


class QuestionManager(models.Manager):
    def _get_optimized_questions(self):
        from questions.models import Answer

        answers_prefetch = Prefetch(
            "answers",
            queryset=Answer.objects.filter(is_active=True).only("id", "question_id")
        )

        return self.select_related('author', 'author__profile') \
                   .prefetch_related('tags', answers_prefetch) \
                   .filter(is_active=True)

    def get_new(self):
        return self._get_optimized_questions().order_by('-updated_at')

    def get_hot(self):
        return self._get_optimized_questions() \
                   .filter(rating__gte=1) \
                   .order_by('-rating')

    def get_by_tag(self, tag_name):
        return self._get_optimized_questions() \
                   .filter(tags__name=tag_name) \
                   .order_by('-updated_at')
