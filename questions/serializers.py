from rest_framework import serializers
from questions.models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'created_at', 'updated_at', 'tags', 'author', 'rating', 'is_active']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'created_at', 'updated_at', 'author', 'rating', 'is_correct', 'is_active']
