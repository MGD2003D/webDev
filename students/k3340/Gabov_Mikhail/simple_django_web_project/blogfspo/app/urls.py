from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_info, name='owner_info')
]