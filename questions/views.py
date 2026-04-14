from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'This is the full text for question number {i}. It contains a lot of interesting details.',
        'answers': [
            {
                'id': j,
                'text': f'This is answer number {j} for question {i}',
                'author': f'helper_{j}',
                'rating': j * 2 - 1,
                'date': '2026-04-08',
                'is_correct': j == 1
            } for j in range(1, (i % 4) + 2)
        ],
        'author': f'user{i}',
        'date': f'2024-06-{i:02d}',
        'rating': i * 3,
        'tags' : ['python', 'django'] if i % 2 == 0 else ['javascript', 'react']
    } for i in range(1, 300)
]

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

def index(request):
    page = paginate(QUESTIONS, request, 5)
    return render(request, 'index.html', {'questions': page})

def hot(request):
    page = paginate(QUESTIONS[::-1], request, 5)
    return render(request, 'hot.html', {'questions': page})

def tag(request, tag_name):
    filtered = [q for q in QUESTIONS if tag_name in q['tags']]
    page = paginate(filtered, request, 5)
    return render(request, 'tag.html', {'questions': page, 'tag': tag_name})

def question_detail(request, question_id):
    question = next((q for q in QUESTIONS if q['id'] == question_id), None)
    if question:
        answers_page = paginate(question['answers'], request, 5)
        return render(request, 'question.html', {'question': question, 'answers': answers_page})
    return render(request, 'question.html', {'question': question})

def ask(request):
    return render(request, 'ask.html')
