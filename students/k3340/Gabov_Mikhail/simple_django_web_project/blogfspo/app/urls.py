from django.urls import path, include
from . import views
from .views import OwnerDetailView, CarListView, CarCreateView, CarUpdateView, CarDeleteView, OwnerCreateView, \
    OwnerUpdateView, OwnerDeleteView, UserCreateView, home, AccountView

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
    path('register/', UserCreateView.as_view(), name='user_create'),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rentals/', views.rentals_view, name='rentals'),
    path('rental/<int:rental_id>/end/', views.end_rental, name='end_rental'),
    path('cars/', views.available_cars, name='available_cars'),
    path('account/', AccountView.as_view(), name='account'),
]