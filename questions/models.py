from django.db import models
from django.contrib.auth.models import User
from questions.managers import QuestionManager
from django.utils import timezone

class DefaultModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    @property
    def was_updated(self):
        return (self.updated_at - self.created_at).total_seconds() > 1

    class Meta:
        abstract = True

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Question(DefaultModel):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(max_length=20000, verbose_name='Текст вопроса')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions', verbose_name='Автор')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг', db_index=True)
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name='Теги')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(DefaultModel):
    text = models.TextField(max_length=20000, verbose_name='Текст ответа')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return f"Ответ #{self.id} к вопросу #{self.question_id}"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    class Meta:
        unique_together = ('user', 'question')

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    class Meta:
        unique_together = ('user', 'answer')
