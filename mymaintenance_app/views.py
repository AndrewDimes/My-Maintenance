from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import WorkOrder, Profile, Photo
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm

# for def
from django.contrib.auth.decorators import login_required
# for class
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
    open_work = 0
    sub_work = 0
    closed_work = 0
    all_open_work = 0
    all_sub_work = 0
    all_closed_work = 0
    profile_query = Profile.objects.filter(user=request.user)
    profile = profile_query[0]
    work_orders = WorkOrder.objects.filter(user=request.user)
    work_orders_all = WorkOrder.objects.all()
    for work in work_orders:
        if work.status == 'S':
            sub_work = sub_work + 1
        elif work.status == 'O':
            open_work = open_work + 1
        elif work.status == 'C':
            closed_work = closed_work + 1
    for work in work_orders_all:
        if work.status == 'S':
            all_sub_work = all_sub_work + 1
        elif work.status == 'O':
            all_open_work = all_open_work + 1
        elif work.status == 'C':
            all_closed_work = all_closed_work + 1
    return render(request, 'index.html', {'profile': profile, 'sub_work': sub_work, 'open_work': open_work, 'closed_work': closed_work, 'all_sub_work': all_sub_work, 'all_open_work': all_open_work, 'all_closed_work': all_closed_work})


def maintenance(request):
    sub_work = []
    super_sub_work = []
    work_orders = WorkOrder.objects.filter(user=request.user)
    for work in work_orders:
        if(work.status == 'S'):
            sub_work.append(work)
    work_orders_all = WorkOrder.objects.all()
    for work in work_orders_all:
        if(work.status == 'S'):
            super_sub_work.append(work)
    page = request.GET.get('page', 1)
    paginator = Paginator(super_sub_work, 6)
    paginator_two = Paginator(sub_work, 5)
    try:
      work = paginator.page(page)
      work_resident = paginator_two.page(page)
    except PageNotAnInteger:
      work = paginator.page(1)
      work_resident = paginator_two.page(1)
    except EmptyPage:
      work = paginator.page(paginator.num_pages)
      work_resident = paginator_two.page(paginator_two.num_pages)
    return render(request, 'maintenance.html', 
    {'work': work, 'work_resident': work_resident})

def open_maintenance(request):
    open_work = []
    super_open_work = []
    work_orders = WorkOrder.objects.filter(user=request.user)
    for work in work_orders:
        if(work.status == 'O'):
            open_work.append(work)   
    work_orders_all = WorkOrder.objects.all()
    for work in work_orders_all:
        if(work.status == 'O'):
            super_open_work.append(work)   
    page = request.GET.get('page', 1)
    paginator = Paginator(super_open_work, 6)
    paginator_two = Paginator(open_work, 5)
    try:
      work = paginator.page(page)
      work_resident = paginator_two.page(page)
    except PageNotAnInteger:
      work = paginator.page(1)
      work_resident = paginator_two.page(1)
    except EmptyPage:
      work = paginator.page(paginator.num_pages)
      work_resident = paginator_two.page(paginator_two.num_pages)
    return render(request, 'maintenance.html', 
    { 'work': work, 'work_resident': work_resident })

def closed_maintenance(request):
    closed_work = []
    super_closed_work = []
    work_orders = WorkOrder.objects.filter(user=request.user)
    for work in work_orders:
        if(work.status == 'C'):
            closed_work.append(work)
    work_orders_all = WorkOrder.objects.all()
    for work in work_orders_all:
        if(work.status == 'C'):
            super_closed_work.append(work)
    page = request.GET.get('page', 1)
    paginator = Paginator(super_closed_work, 6)
    paginator_two = Paginator(closed_work, 5)
    try:
      work = paginator.page(page)
      work_resident = paginator_two.page(page)
    except PageNotAnInteger:
      work = paginator.page(1)
      work_resident = paginator_two.page(1)
    except EmptyPage:
      work = paginator.page(paginator.num_pages)
      work_resident = paginator_two.page(paginator_two.num_pages)
    return render(request, 'maintenance.html', 
    {'work': work, 'work_resident': work_resident})

def work_order_details(request, work_order_id):
    work_order = WorkOrder.objects.get(id=work_order_id)
    profile = Profile.objects.get(user=work_order.user)
    
    comment_form = CommentForm()
    return render(request, 'work_order_details.html', {
        'work_order': work_order,
        'comment_form': comment_form,
        'profile': profile
    })

def add_comment(request, work_order_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.work_order_id = work_order_id
    new_comment.save()
  return redirect('work_order_details', work_order_id=work_order_id)


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


def workorder_status(request, work_order_id):
    work_order = WorkOrder.objects.get(id=work_order_id)
    if work_order.status == 'O':
        work_order.status = 'C'
        work_order.save()
    if work_order.status == 'S':
        work_order.status = 'O'
        work_order.save()
    print(work_order.status)

    return redirect('work_order_details', work_order_id=work_order_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
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
        key = uuid.uuid4().hex[:6] + \
        photo_file.name[photo_file.name.rfind('.'):]
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
