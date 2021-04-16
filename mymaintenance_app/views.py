from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import WorkOrder, Profile
#for def
from django.contrib.auth.decorators import login_required
#for class
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return redirect('login')

def index(request):
  return render(request, 'index.html')

def maintenance(request):
  work_orders = WorkOrder.objects.filter(user=request.user)
  return render(request, 'maintenance.html', {'work_orders':work_orders})

def profile(request):
  return render(request, 'profile.html')

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = ['full_name', 'phone', 'apartment']

  def form_valid(self, form):
    form.instance.user = self.request.user

    return super().form_valid(form)

class WorkOrderCreate(LoginRequiredMixin, CreateView):
  model = WorkOrder
  fields = ['title', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user

    return super().form_valid(form)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('profile_create')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)