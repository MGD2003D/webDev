from django.urls import path
from . import views
from .views import OwnerDetailView, CarListView, CarCreateView, CarUpdateView, CarDeleteView, OwnerCreateView, \
    OwnerUpdateView, OwnerDeleteView

urlpatterns = [
    # path('owner/<int:owner_id>/', views.owner_info, name='owner_info'),
    path('owner/list/', views.owner_list, name='owner_list'),
    path('owner/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('car/list/', CarListView.as_view(), name='car_list'),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name = 'car_delete'),
    path('owner/create/', OwnerCreateView.as_view(), name='owner_create'),
    path('owner/<int:pk>/update/', OwnerUpdateView.as_view(), name='owner_update'),
    path('owner/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
]