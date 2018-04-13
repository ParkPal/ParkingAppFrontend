from django.urls import path

from . import views
import polls.views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(r'logout/', polls.views.logout_view, name = 'logout'),
    path(r'login/', polls.views.login_view, name='login' ),
    path(r'signup/', polls.views.signup_view, name='signup' ),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    #path(r'', views.DashView.as_view(), name='dash'),
    #path('<user_username>/dashboard/', views.OwnerDashView.as_view(), name = 'owner_dash'),
    path('<user_username>/<host_lotName>/lot_report', polls.views.lot_graph_view, name = 'lot_graph_view'),
    path('owner_dashboard', polls.views.owner_view, name = 'owner_dash'),
]
