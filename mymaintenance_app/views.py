from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import WorkOrder, Profile, Photo
from .forms import WorkOrderForm
#for def
from django.contrib.auth.decorators import login_required
#for class
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3  

# Create your views here.
S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'pincollector'


def home(request):
  if request.user.is_authenticated:
      return redirect('index')
  else:
    return redirect('login')

def index(request):
  profile_query = Profile.objects.filter(user=request.user)
  profile = profile_query[0]
  print(profile)
  return render(request, 'index.html', {'profile':profile})

def maintenance(request):
  work_orders = WorkOrder.objects.filter(user=request.user)
  work_orders_all = WorkOrder.objects.all()
  return render(request, 'maintenance.html', {'work_orders':work_orders, 'work_orders_all': work_orders_all})

def work_order_details(request, work_order_id):
  work_order = WorkOrder.objects.get(id=work_order_id)

  
  return render(request, 'work_order_details.html', {
    'work_order': work_order
  })

def profile(request):
  return render(request, 'profile.html')

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = ['full_name', 'phone', 'apartment', 'email']

  def form_valid(self, form):
    form.instance.user = self.request.user

    return super().form_valid(form)

class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = Profile
  fields = ['phone', 'apartment', 'email']

class WorkOrderCreate(LoginRequiredMixin, CreateView):
  model = WorkOrder
  fields = ['title', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user

    return super().form_valid(form)

def workorder_update(request,work_order_id):
  form = WorkOrderForm(request.POST)
  if form.is_valid():
    work_order = WorkOrder.objects.get(id=work_order_id)
    work_order.status = form.save(commit=False)
  return render(request, 'status_form.html', {'work_order_id':work_order_id, 'form' : form})

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

def add_photo(request, work_order_id):
    # photo-file will be the "name" attribute on the <input type="file">
    
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, work_order_id=work_order_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('work_order_details', work_order_id=work_order_id)

