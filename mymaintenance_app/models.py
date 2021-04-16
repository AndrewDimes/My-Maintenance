from django.db import models

# Create your models here.
class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        full_name = models.CharField(max_length=100)
        phone = models.IntegerField()
        apartment = models.CharField(max_length=10)
        work_orders = models.OneToManyField(WorkOrder)

STATUS = (
    ('S', 'Submitted'),
    ('O', 'Open'),
    ('C', 'Complete')
)

class WorkOrder(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
    max_length=1,
    choices=STATUS,
    default=STATUS[0][0]
  ) 