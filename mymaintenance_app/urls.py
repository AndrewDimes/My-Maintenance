from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('profile/', views.profile, name='profile'),
]