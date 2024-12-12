from django.urls import path
from .views import ESearchView

app_name = 'search'

urlpatterns = [
    path('', ESearchView.as_view(), name='index'),
]