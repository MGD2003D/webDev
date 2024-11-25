from django.urls import path
from . import views
from .views import OwnerDetailView, CarListView, create_view

urlpatterns = [
    # path('owner/<int:owner_id>/', views.owner_info, name='owner_info'),
    path('owner/list/', views.owner_list, name='owner_list'),
    path('owner/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('car/list/', CarListView.as_view(), name='car_list'),
    path('car/create/', create_view, name='car_create'),
]