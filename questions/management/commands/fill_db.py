from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile
from questions.models import Question, Answer, Tag, QuestionLike
from faker import Faker
import random

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
        users = [User(username=fake.unique.user_name(), email=fake.email(), password='password123') for _ in range(users_count)]
        User.objects.bulk_create(users, batch_size=5000)

        saved_users = list(User.objects.all())
        profiles = [Profile(user=u) for u in saved_users]
        Profile.objects.bulk_create(profiles, batch_size=5000)

        self.stdout.write('Creating tags...')
        tags = [Tag(name=fake.unique.word() + str(i)) for i in range(tags_count)]
        Tag.objects.bulk_create(tags, batch_size=5000)
        saved_tags = list(Tag.objects.all())

        self.stdout.write('Creating questions...')
        questions = [
            Question(
                title=fake.sentence()[:255],
                text=fake.text(),
                author=random.choice(saved_users),
            ) for _ in range(questions_count)
        ]
        Question.objects.bulk_create(questions, batch_size=5000)
        saved_questions = list(Question.objects.all())

        # Проставление ManyToMany для тегов (по 2-3 тега на вопрос)
        self.stdout.write('Adding tags to questions...')
        ThroughModel = Question.tags.through
        question_tags = []
        for q in saved_questions:
            q_tags = random.sample(saved_tags, k=random.randint(1, 3))
            for t in q_tags:
                question_tags.append(ThroughModel(question_id=q.id, tag_id=t.id))
        ThroughModel.objects.bulk_create(question_tags, batch_size=10000)

        self.stdout.write('Creating answers...')
        answers = [
            Answer(
                text=fake.text(),
                author=random.choice(saved_users),
                question=random.choice(saved_questions),
            ) for _ in range(answers_count)
        ]
        Answer.objects.bulk_create(answers, batch_size=10000)

        self.stdout.write(self.style.SUCCESS('Database successfully filled!'))
