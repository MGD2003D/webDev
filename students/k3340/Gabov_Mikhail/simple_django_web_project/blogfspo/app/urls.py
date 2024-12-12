from django.urls import path, include
from . import views
from .views import OwnerDetailView, CarListView, CarCreateView, CarUpdateView, OwnerCreateView, \
    OwnerUpdateView, UserCreateView, AccountView, car_delete, delete_owner
# from .views import CarDeleteView, OwnerDeleteView

urlpatterns = [
    # path('owner/<int:owner_id>/', views.owner_info, name='owner_info'),
    path('owner/list/', views.owner_list, name='owner_list'),
    path('owner/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('car/list/', CarListView.as_view(), name='car_list'),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    # path('car/<int:pk>/delete/', CarDeleteView.as_view(), name = 'car_delete'),
    path('car/<int:pk>/delete/', car_delete, name='delete_car'),
    path('owner/create/', OwnerCreateView.as_view(), name='owner_create'),
    path('owner/<int:pk>/update/', OwnerUpdateView.as_view(), name='owner_update'),
    # path('owner/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
    path('owner/<int:owner_id>/delete/', delete_owner, name='delete_owner'),
    path('register/', UserCreateView.as_view(), name='user_create'),
    path('', views.role_redirect, name='role_redirect'),
    path('user/home/', views.home, name='home_user'),
    path('admin/home/', views.admin_home, name='home_admin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rentals/', views.rentals_view, name='rentals'),
    path('rental/<int:rental_id>/end/', views.end_rental, name='end_rental'),
    path('cars/', views.available_cars, name='available_cars'),
    path('account/', AccountView.as_view(), name='account'),
    path('manage_rentals/', views.manage_rentals, name='manage_rentals'),
    path('rental/<int:rental_id>/update/', views.update_rental, name='update_rental'),
    path('rental/<int:rental_id>/delete/', views.delete_rental, name='delete_rental'),
    path('rental/add/', views.add_rental, name='add_rental'),
    path('user_create_modal/', views.user_create_modal, name='user_create_modal'),
]