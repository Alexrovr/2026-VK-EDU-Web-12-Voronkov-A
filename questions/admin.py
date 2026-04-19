from django.contrib import admin
from .models import Question, Answer, Tag

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1
    raw_id_fields = ('author',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('created_at',)
    raw_id_fields = ('author',)
    inlines = [AnswerInline]

admin.site.register(Tag)
admin.site.register(Answer)
