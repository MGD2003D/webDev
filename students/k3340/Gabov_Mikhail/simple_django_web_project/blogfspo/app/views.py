from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Owner, Car, CarOwner, User
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import CarCreateForm, OwnerCreateForm, UserRegistrationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def owner_info(request, owner_id):
    try:
        owner = Owner.objects.get(id = owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner not found")

    return render(request, 'app/ownersearch.html', {'owner': owner})

def owner_list(request):
    context = {}

    context['owner'] = Owner.objects.all()

    return render(request, 'app/ownerlist.html', context)


class OwnerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Owner
    template_name = 'app/owner_detail.html'
    permission_required = 'app.view_owner'

    def get_object(self, queryset=None):
        owner = get_object_or_404(Owner, user=self.request.user)

        if not self.request.user.has_perm('app.view_owner', owner):
            raise PermissionDenied("У вас нет доступа к этому объекту.")

        return owner


class CarListView(ListView):
    model = Car

    def get_queryset(self):
        owner_id = self.request.GET.get('owner')

        if owner_id:
            try:
                owner_id = int(owner_id)

                car_ids = CarOwner.objects.filter(owner_id=owner_id).values_list('car_id', flat=True)

                return Car.objects.filter(id__in=car_ids)

            except ValueError:
                return self.model.objects.none()

        return Car.objects.all()

"""
def CarCreateView(request):

    context={}

    form = CarPostForm(request.POST or None)

    if form.is_valid():

        form.save()
    context['form'] = form
    return render(request, 'app/car_create.html', context)
"""

class CarCreateView(CreateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'app/car_create.html'
    success_url = '/app/car/list'

class CarUpdateView(UpdateView):
    model = Car
    fields = ['license_plate', 'brand', 'model', 'color']
    success_url = '/app/car/list'
    template_name = 'app/car_update.html'

class CarDeleteView(DeleteView):
    model = Car
    success_url = '/app/car/list'
    template_name = 'app/car_delete.html'

class OwnerCreateView(CreateView):
    model = Owner
    form_class = OwnerCreateForm
    success_url = '/app/owner/list'
    template_name = 'app/owner_create.html'

class OwnerUpdateView(UpdateView):
    model = Owner
    fields = ['last_name', 'first_name', 'birth_date']
    success_url = '/app/owner/list'
    template_name = 'app/owner_update.html'

class OwnerDeleteView(DeleteView):
    model = Owner
    success_url = '/app/owner/list'
    template_name = 'app/owner_delete.html'

class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'app/register.html'

@login_required
def home(request):
    if request.user.is_superuser:
        role = "Admin"
    else:
        role = "User"
    return render(request, 'app/home.html', {'role': role})