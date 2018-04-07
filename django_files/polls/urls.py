from django.urls import path

from . import views
import polls.views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(r'login/', polls.views.login_view, name='login' ),
    path(r'signup/', polls.views.signup_view, name='signup' ),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    #path(r'', views.DashView.as_view(), name='dash'),
    path('<host_lotName>/dash/', views.DashView.as_view(), name='lot_dash'),
    path('<user_username>/dash/', views.OwnerDashView.as_view(), name = 'owner_dash')
]
