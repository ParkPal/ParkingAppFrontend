from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
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


def login_view(request):
    if request.user.is_authenticated:
        #return HttpResponseRedirect(reverse('polls:owner_dash'))
        return render(request, 'polls/owner_dash.html', {
            'user':request.user,
        })
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                #return HttpResponseRedirect(reverse('polls:owner_dash'))
                return render(request, 'polls/owner_dash.html', {
                    'user':request.user,
                })
                
            else:
                failed = "User not found!"
                content = {'error':failed}
                return render(request, 'polls/login.html')

        else:
            return render(request, 'polls/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'polls/new_dash.html',{
        'latest_host_list': Host.objects.order_by('lastConnect')[:5],
    })
def signup_view(request):
    if request.method == 'POST':
        if request.POST['pwd_1'] == request.POST['pwd_2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'polls/signup.html', {'error': 'Username already in use!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password = request.POST['pwd_1'])
                login(request, user)
                return render(request, 'polls/owner_dash.html')
        else:
            return render(request, 'polls/signup.html', {'error': 'Passwords didn\'t match!'})
    else:
        return render(request, 'polls/signup.html')





class IndexView(generic.ListView):
    template_name = 'polls/new_dash.html'
    context_object_name = 'latest_host_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Host.objects.order_by('lastConnect')[:5]


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
        """Return the last five connected hosts."""
        return Host.objects.order_by('lastConnect')[:5]
#view for owner viewing all their owned lots
class OwnerDashView(generic.ListView):
    template_name = 'polls/owner_dash.html'
    context_object_name = 'owned_host_list'
    

    def get_queryset(self):
        #u = get_object_or_404(User, pk = self.request.user.id)
        return self.request.user.host_set.all()
#
class LotDashView(generic.ListView):
 
    model = Host
    template_name = 'polls/lot_dash.html'
    context_object_name = 'host_node_list'
    

    def get_queryset(self):
        return self.request.user.host_set.all()
#View for a 
def lot_graph_view(request,  host_id):
    if request.user.is_authenticated:
        host = get_object_or_404(Host, pk=host_id)
        return render(request, 'polls/lot_dash.html', { 'host':host, })
    else:
        return render(request, 'polls/new_dash.html',{
            'latest_host_list':  Host.objects.order_by('lastConnect'),
        })
    
     
     # this is how we would access host history in the template
     # host.history_set.all()
     # Could access nodes beloging to the host in this manner

def owner_view(request):
    if request.user.is_authenticated:
        return render(request, 'polls/owner_dash.html', {
            'user':request.user,
        })
    else:
        return render(request, 'polls/new_dash.html',{
            'latest_host_list':  Host.objects.order_by('lastConnect'),
        })
    
            


                
            
