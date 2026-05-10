from django import forms
from .models import Question, Answer, Tag

class AskForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Введите теги через запятую",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'python, django, ...'})
    )

    class Meta:
        model = Question
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кратко опишите суть'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

    def save(self, author=None, commit=True):
        question = super().save(commit=False)
        if author:
            question.author = author
        if commit:
            question.save()
            tags_list = self.cleaned_data['tags'].split(',')
            question.tags.clear()
            for tag_name in tags_list:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    question.tags.add(tag)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Напишите ответ...', 'class': 'answer-form__textarea', 'required': True}),
        }
