from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Tag


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)

def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request, 20)
    return render(request, 'index.html', {'questions': page})

def hot(request):
    questions = Question.objects.get_hot()
    page = paginate(questions, request, 20)
    return render(request, 'hot.html', {'questions': page})

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.get_by_tag(tag_name)
    page = paginate(questions, request, 20)
    return render(request, 'tag.html', {'questions': page, 'tag': tag})

def question_detail(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author', 'author__profile').prefetch_related('tags'), pk=question_id)
    answers = question.answers.select_related('author', 'author__profile').filter(is_active=True).order_by('-updated_at')
    page = paginate(answers, request, 30)
    return render(request, 'question.html', {'question': question, 'answers': page})

def ask(request):
    return render(request, 'ask.html')
