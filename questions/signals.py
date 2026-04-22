from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import QuestionLike, AnswerLike

@receiver([post_save, post_delete], sender=QuestionLike)
def update_question_rating(sender, instance, **kwargs):
    question = instance.question
    new_rating = QuestionLike.objects.filter(question=question).aggregate(Sum('value'))['value__sum'] or 0
    question.__class__.objects.filter(pk=question.pk).update(rating=new_rating)

@receiver([post_save, post_delete], sender=AnswerLike)
def update_answer_rating(sender, instance, **kwargs):
    answer = instance.answer
    new_rating = AnswerLike.objects.filter(answer=answer).aggregate(Sum('value'))['value__sum'] or 0
    answer.__class__.objects.filter(pk=answer.pk).update(rating=new_rating)
