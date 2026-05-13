from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from questions.forms import AskForm, AnswerForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from questions.models import Question, Tag, Answer
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import DetailView
from questions.serializers import QuestionSerializer, AnswerSerializer


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


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question.html'
    context_object_name = 'question'
    pk_url_kwarg = 'question_id'

    def get_queryset(self):
        return super().get_queryset().select_related('author__profile').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers_qs = Answer.objects.filter(is_active=True, question=self.object)\
            .select_related('author__profile')\
            .order_by('-updated_at')

        paginator = Paginator(answers_qs, 30)
        page_number = self.request.GET.get('page')
        context['answers'] = paginator.get_page(page_number)
        context['answer_form'] = AnswerForm()
        return context

class AnswerCreateAPI(CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        serializer.save(author=self.request.user, question=question)

class QuestionUpdateAPI(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'question_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

class AnswerUpdateAPI(UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'answer_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class AskView(LoginRequiredMixin, FormView):
    template_name = 'ask.html'
    form_class = AskForm

    def form_valid(self, form):
        question = form.save(author=self.request.user)
        return redirect(reverse('question_detail', kwargs={'question_id': question.id}))
