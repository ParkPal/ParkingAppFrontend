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

        #> data
        host = get_object_or_404(Host, pk=host_id)
        lotHistory = {}
        
        for h in host.history_set.all():
            lotHistory.update({ h.lastConnect : (h.spotsInUse)/(h.totalSpots) })
        
        


        #> Graphs
        
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
            defined chart
            chart: defined chart type
            title, xAxis, yAxis:
            series: plot the data
        """
        chart = {
            'chart': {'type': 'area'},
            'title': {'text': 'Lot Usage by Time'},
            'xAxis': {'categories': xData},
            'yAxis': { 'title': { 'text': 'Spots in Use'}, 'visible': 'true' },
            'series': [yAxis],
            }
        '''
        x = {
            'name': 'History',
            'data': xData,
            'color': '#1E90FF',
            'visible': 'true'
        }
        y = {
            'name': "Percent In Use",
            'data': yData,
            'color': '#1E90FF',
            'visible': 'true',
        }

        chart = {
            'chart': {'type': 'area'},
            'title': {'text': 'Percent In Use Over Time'},
            'xAxis': { 'x': x },
            'yAxis': { 'y': y },
            'series': [{
                name: 'Time'
            }, yData]
            }
        '''
        '''
        chart = {
            type: 'area'
            },
        title = {
            text = "US and USSR nuclear stockpiles"
        },
        yAxis = {
            title = {
                text =  "Nuclear weapon states"
            },
            labels = {
                formatter = function () {
                    return this.value / 1000 + 'k';
                }
            }
        },
        tooltip = {
            pointFormat = "{series.name} had stockpiled <b>{point.y:,.0f}</b><br/>warheads in {point.x}"
        },
        plotOptions = {
            area = {
                pointStart = 1940,
                marker = {
                    enabled = false,
                    symbol = 'circle',
                    radius = 2,
                    states = {
                        hover = {
                            enabled = true
                        }
                    }
                }
            }
        },
        series = [{
            name = 'USA',
            data = [
                null, null, null, null, null, 6, 11, 32, 110, 235,
                369, 640, 1005, 1436, 2063, 3057, 4618, 6444, 9822, 15468,
                20434, 24126, 27387, 29459, 31056, 31982, 32040, 31233, 29224, 27342,
                26662, 26956, 27912, 28999, 28965, 27826, 25579, 25722, 24826, 24605,
                24304, 23464, 23708, 24099, 24357, 24237, 24401, 24344, 23586, 22380,
                21004, 17287, 14747, 13076, 12555, 12144, 11009, 10950, 10871, 10824,
                10577, 10527, 10475, 10421, 10358, 10295, 10104, 9914, 9620, 9326,
                5113, 5113, 4954, 4804, 4761, 4717, 4368, 4018
            ]
        }, {
            name = 'USSR/Russia',
            data = [null, null, null, null, null, null, null, null, null, null,
                   5, 25, 50, 120, 150, 200, 426, 660, 869, 1060,
                   1605, 2471, 3322, 4238, 5221, 6129, 7089, 8339, 9399, 10538,
                   11643, 13092, 14478, 15915, 17385, 19055, 21205, 23044, 25393, 27935,
                   30062, 32049, 33952, 35804, 37431, 39197, 45000, 43000, 41000, 39000,
                   37000, 35000, 33000, 31000, 29000, 27000, 25000, 24000, 23000, 22000,
                   21000, 20000, 19000, 18000, 18000, 17000, 16000, 15537, 14162, 12787,
                   12600, 11400, 5500, 4512, 4502, 4502, 4500, 4500
            ]
        }]
        '''
        
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
    
            


                
            
