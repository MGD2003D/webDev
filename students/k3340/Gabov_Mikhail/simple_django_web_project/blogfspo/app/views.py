from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Owner, Car, CarOwner
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import CarCreateForm, OwnerCreateForm

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

class OwnerDetailView(DetailView):
    model = Owner


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