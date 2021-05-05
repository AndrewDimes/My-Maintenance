from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('profile/', views.profile, name='profile'),
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name="profile_update"),
    path('workorders/create/', views.WorkOrderCreate.as_view(), name='workorder_create'),
    path('workorders/<int:work_order_id>/status', views.workorder_status, name="status"),
    path('workorders/<int:work_order_id>/' , views.work_order_details, name="work_order_details"),
    path('workorders/<int:work_order_id>/add_photo',views.add_photo, name="add_photo"),
    path('workorders/<int:work_order_id>/add_comment', views.add_comment, name="add_comment"),
]