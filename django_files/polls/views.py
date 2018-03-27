from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Host, Node


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class DashView(generic.ListView):
    template_name = 'polls/new_dash.html'
    context_object_name = 'latest_host_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Host.objects.order_by('lastConnect')[:5]

class LotDashView(generic.DetailView):
    model = Host
    template_name = 'polls/lot_dash.html'

def login(request):
    if request.user.is_authenticated:
        return index(request)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return render(request, 'new_dash.html')
            else:
                failed = "User not found!"
                content = {'error':failed}
                return render(request, 'login.html')

        else:
            return render(request, 'login.html')

def logout(request):
    logout(request)
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['pwd_1'] == request.POST['pwd_2']
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username already in use!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password = request.POST[pwd_1])
                login(request, user)
                return render(request, 'new_dash.html')
        else:
            return render(request, 'signup.html', {'error': 'Passwords didn\'t match!'})
    else:
        return render(request, 'signup.html')
                
            
