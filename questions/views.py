from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AskForm, AnswerForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Tag, Answer


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

    if request.method == 'POST' and 'edit_question' in request.POST:
        if request.user == question.author:
            form = AskForm(request.POST, instance=question)
            if form.is_valid():
                form.save(commit=False)
                question.save()
        return redirect('question_detail', question_id=question_id)

    if request.method == 'POST' and 'edit_answer' in request.POST:
        answer_id = request.POST.get('answer_id')
        answer = get_object_or_404(Answer, pk=answer_id)
        if request.user == answer.author:
            form = AnswerForm(request.POST, instance=answer)
            if form.is_valid():
                form.save()
        return redirect('question_detail', question_id=question_id)

    if request.method == 'POST' and 'new_answer' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question_id)
    else:
        form = AnswerForm()

    answers = question.answers.select_related('author', 'author__profile').filter(is_active=True).order_by('-updated_at')
    page = paginate(answers, request, 30)

    return render(request, 'question.html', {'question': question, 'answers': page, 'form': form})

def ask(request):
    form = AskForm(request.POST or None)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if form.is_valid():
            question = form.save(author=request.user)
            return redirect('question_detail', question_id=question.id)

    return render(request, 'ask.html', {'form': form})
