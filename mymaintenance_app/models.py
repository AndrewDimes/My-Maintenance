from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

# Create your models here.
STATUS = (
    ('S', 'Submitted'),
    ('O', 'Open'),
    ('C', 'Complete')
)

class WorkOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
    max_length=1,
    choices=STATUS,
    default=STATUS[0][0]
  )
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('maintenance')


class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        full_name = models.CharField(max_length=100)
        phone = models.CharField(max_length=10)
        apartment = models.CharField(max_length=10)
        work_orders = models.ManyToManyField(WorkOrder)
        def __str__(self):
            return self.full_name

        def get_absolute_url(self):
            return reverse('index')



