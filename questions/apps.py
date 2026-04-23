from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    name = 'questions'


class LikesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'likes'

    def ready(self):
        import likes.signals
