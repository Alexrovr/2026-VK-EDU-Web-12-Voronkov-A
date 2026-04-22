from django.contrib import admin
from .models import Question, Answer, Tag, QuestionLike, AnswerLike

class QuestionLikeInline(admin.TabularInline):
    model = QuestionLike
    extra = 0
    raw_id_fields = ('user',)

class AnswerLikeInline(admin.TabularInline):
    model = AnswerLike
    extra = 0
    raw_id_fields = ('user',)

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1
    raw_id_fields = ('author',)
    show_change_link = True

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('created_at',)
    raw_id_fields = ('author',)
    inlines = [AnswerInline, QuestionLikeInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'rating', 'created_at', 'is_correct')
    search_fields = ('text',)
    list_filter = ('is_correct', 'created_at')
    raw_id_fields = ('author', 'question')
    inlines = [AnswerLikeInline]

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'value')
    raw_id_fields = ('user', 'question')

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'value')
    raw_id_fields = ('user', 'answer')

admin.site.register(Tag)
