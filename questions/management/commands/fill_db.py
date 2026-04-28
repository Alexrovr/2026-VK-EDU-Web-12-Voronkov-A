from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile
from django.db import transaction
from django.db.models import F, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
import random
import uuid

class Command(BaseCommand):
    help = 'Fills the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        users_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio

        self.stdout.write('Creating users...')
        users = []
        for _ in range(users_count):
            unique_suffix = uuid.uuid4().hex[:8]
            users.append(User(
                username=f"{fake.unique.user_name()}_{unique_suffix}",
                email=fake.email(),
                password='password123',
            ))
        User.objects.bulk_create(users, batch_size=5000)

        user_ids = list(User.objects.order_by('-id').values_list('id', flat=True)[:users_count])
        profiles = [Profile(user_id=u, bio=fake.text(max_nb_chars=200)) for u in user_ids]
        Profile.objects.bulk_create(profiles, batch_size=5000)

        self.stdout.write('Creating tags...')
        tags = [Tag(name=f"{fake.word()}_{uuid.uuid4().hex[:5]}") for i in range(tags_count)]
        Tag.objects.bulk_create(tags, batch_size=5000)
        tag_ids = list(Tag.objects.order_by('-id').values_list('id', flat=True)[:tags_count])

        self.stdout.write('Creating questions...')
        questions = []
        for _ in range(questions_count):
            created_at = fake.date_time_this_year()
            questions.append(Question(
                title=fake.sentence()[:255],
                text=fake.text(),
                author_id=random.choice(user_ids),
                created_at=created_at,
                updated_at=created_at,
            ))
        Question.objects.bulk_create(questions, batch_size=5000)
        question_ids = list(Question.objects.order_by('-id').values_list('id', flat=True)[:questions_count])
        # Question.objects.filter(id__in=question_ids).update(updated_at=F('created_at'))

        self.stdout.write('Adding tags to questions...')
        ThroughModel = Question.tags.through
        question_tags = []
        for q in question_ids:
            q_tags = random.sample(tag_ids, k=random.randint(1, 3))
            # q_tags = random.sample(tag_ids, k=random.randint(1, min(3, len(tag_ids))))
            for t in q_tags:
                question_tags.append(ThroughModel(question_id=q, tag_id=t))
        ThroughModel.objects.bulk_create(question_tags, batch_size=10000)

        self.stdout.write('Creating answers...')
        answers = []
        for _ in range(answers_count):
            created_at = fake.date_time_this_year()
            answers.append(Answer(
                text=fake.text(),
                author_id=random.choice(user_ids),
                question_id=random.choice(question_ids),
                created_at=created_at,
                updated_at=created_at,
                is_correct=random.choice([True, False]),
            ))
        Answer.objects.bulk_create(answers, batch_size=10000)
        answer_ids = list(Answer.objects.order_by('-id').values_list('id', flat=True)[:answers_count])
        # Answer.objects.filter(id__in=answer_ids).update(updated_at=F('created_at'))

        unique_question_likes = set()
        while len(unique_question_likes) < questions_count * 5:
            u_id = random.choice(user_ids)
            q_id = random.choice(question_ids)
            unique_question_likes.add((u_id, q_id))
        question_likes = [
            QuestionLike(user_id=u_id, question_id=q_id, value=random.choice([1, 1, 1, -1]))
            for u_id, q_id in unique_question_likes
        ]

        with transaction.atomic():
            QuestionLike.objects.bulk_create(question_likes, batch_size=5000)
            likes_sum = QuestionLike.objects.filter(
                question=OuterRef('pk')
            ).values('question').annotate(
                total=Sum('value')
            ).values('total')
            Question.objects.update(
                rating=Coalesce(Subquery(likes_sum), 0)
            )

        unique_answer_likes = set()
        while len(unique_answer_likes) < answers_count * 5:
            u_id = random.choice(user_ids)
            a_id = random.choice(answer_ids)
            unique_answer_likes.add((u_id, a_id))
        answer_likes = [
            AnswerLike(user_id=u_id, answer_id=a_id, value=random.choice([1, 1, 1, -1]))
            for u_id, a_id in unique_answer_likes
        ]

        with transaction.atomic():
            AnswerLike.objects.bulk_create(answer_likes, batch_size=5000)
            likes_sum = AnswerLike.objects.filter(
                answer=OuterRef('pk')
            ).values('answer').annotate(
                total=Sum('value')
            ).values('total')
            Answer.objects.update(
                rating=Coalesce(Subquery(likes_sum), 0)
            )

        self.stdout.write(self.style.SUCCESS('Database successfully filled!'))
