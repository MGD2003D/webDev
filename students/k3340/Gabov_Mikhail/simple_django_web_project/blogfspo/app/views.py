from django.http import Http404
from django.shortcuts import render
from .models import Owner, Car, CarOwner
from django.views.generic import DetailView, ListView

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