from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from polls.models import Question, Choice

from django.http import HttpResponse

# Create your views here.

def index (request):
    context = {'titulo': 'Página Principal'}
    return render(request, 'home.html', context)

@login_required # controle de acesso usando o decorador de função
def sobre (request):
    return HttpResponse('Olá, este é um app de enquete')

def exibe_questao(request, question_id):
    question = Question.objects.get(id=question_id)

    if question is not None:
        #questao.question_text
        return HttpResponse(f'{question.question_text}')
    
    return HttpResponse('Não existe questão a exibir')

def ultimas_perguntas(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    #return render(request, 'polls/perguntas.html', context)
    return render(request, 'perguntas_recentes.html', context)
    
class QuestionCreateView(CreateView):
    model = Question
    template_name = 'polls/question_form.html'
    fields = ('question_text', 'pub_date', )
    success_url = reverse_lazy('polls_list')
def get_context_data(self, **kwargs):
    context = super(QuestionCreateView, self).get_context_data(**kwargs)
    context['form_title'] = 'Criando uma pergunta'
    return context

class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'polls/question_form.html'
    fields = ('question_text', 'pub_date', )
    success_url = reverse_lazy('polls_list')
def get_context_data(self, **kwargs):
    context = super(QuestionUpdateView, self).get_context_data(**kwargs)
    context['form_title'] = 'Editando a pergunta'
    return context

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete_form.html'
    success_url = reverse_lazy('polls_all')
    success_message = 'Pergunta excluída com sucesso.'
def form_valid(self, request, *args, **kwargs):
    messages.success(self.request, self.success_message)
    return super(QuestionDeleteView, self).form_valid(request, *args, **kwargs)

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/question_detail.html'
    context_object_name = 'question'

class QuestionListView(ListView):
    model = Question
    template_name = 'polls/question_list.html'
    context_object_name = 'questions'
    paginate_by = 5 # quantidade de itens por página
    ordering = ['-pub_date'] # ordenar pela data de publicação de forma inversão

class SobreTemplateView(TemplateView):
    template_name = 'polls/sobre.html'