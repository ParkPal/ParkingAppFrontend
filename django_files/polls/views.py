from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.http import Http404
from django.urls import reverse
from django.views import generic
import json

from .models import Choice, Question, Host, Node

#Boiler plate view example
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

#User session views
def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'polls/owner_dash.html', {
            'user':request.user,
        })
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)
            if user is not None: #User exists
                login(request, user)
                return render(request, 'polls/owner_dash.html', {
                    'user':request.user,
                })
                
            else: #User does not exist
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




# Driver dashboard view
class IndexView(generic.ListView):
    template_name = 'polls/new_dash.html'
    context_object_name = 'latest_host_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Host.objects.order_by('lastConnect')[:5]

# Boiler plate generic views
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class OwnerDashView(generic.ListView):
    template_name = 'polls/owner_dash.html'
    context_object_name = 'owned_host_list' # How object will be accessed in template
    

    def get_queryset(self):
        #Return set of all hosts with a fk to the given user
        return self.request.user.host_set.all()
class LotDashView(generic.ListView):
 
    model = Host
    template_name = 'polls/lot_dash.html'
    context_object_name = 'host_node_list'
    

    def get_queryset(self):
        return self.request.user.host_set.all()
#Detail view of an individual lot
def lot_graph_view(request,  host_id):
    if request.user.is_authenticated:

        # Template data
        host = get_object_or_404(Host, pk=host_id)
        lotHistory = {}
        
        for h in host.history_set.all():
            lotHistory.update({ h.lastConnect : (h.spotsInUse)/(h.totalSpots) })
        
        


        # Graphs
        
        xData = list()
        yData = list()

        for date, inUse in lotHistory.items():
            xData.append(str(date))
            yData.append(inUse)

        yAxis = {
            'name': 'Overall Lot Usage.',
            'data': yData,
            'color': '#0095ff'
        }

        """
            chart: chart type
            title, xAxis, yAxis:
            series: data to plot
        """
        chart = {
            'chart': {'type': 'area'},
            'title': {'text': 'Lot Usage by Time'},
            'xAxis': {'categories': xData},
            'yAxis': { 'title': { 'text': 'Spots in Use'}, 'visible': 'true' },
            'series': [yAxis],
            }
        
        jsonChart = json.dumps(chart)

        return render(request, 'polls/lot_dash.html', {
              'host':host,
              'chart':jsonChart
          })
    else:
        return render(request, 'polls/new_dash.html',{
            'latest_host_list':  Host.objects.order_by('lastConnect'),
        })
    
     
     # this is how we would access host history in the template
     # host.history_set.all()
     # Could access nodes beloging to the host in this manner

#view for owner viewing all their owned lots
def owner_view(request):
    if request.user.is_authenticated:

        #Render page w/ data
        
        return render(request, 'polls/owner_dash.html', {
            'user':request.user,
        })
    else:
        return render(request, 'polls/new_dash.html',{
            'latest_host_list':  Host.objects.order_by('lastConnect'),
        })
    
            


                
            
