from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Owner, Car, CarOwner, User
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import CarCreateForm, OwnerCreateForm, UserRegistrationForm, CarOwnerForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages

# Create your views here.
def owner_info(request, owner_id):
    try:
        owner = Owner.objects.get(id = owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner not found")

    return render(request, 'app/ownersearch.html', {'owner': owner})

def owner_list(request):
    context = {}

    context['owner'] = Owner.objects.exclude(first_name__isnull=True).exclude(first_name="").exclude(last_name__isnull=True).exclude(last_name="")

    context['users'] = User.objects.exclude(is_staff=True, is_superuser=True).exclude(username="AnonymousUser")

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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Car added successfully!")
        return response


class CarUpdateView(UpdateView):
    model = Car
    fields = ['license_plate', 'brand', 'model', 'color']
    success_url = '/app/car/list'
    template_name = 'app/car_update.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Car updated successfully!")
        return response

class CarDeleteView(DeleteView):
    model = Car
    success_url = '/app/car/list'
    template_name = 'app/car_delete.html'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Car deleted successfully!")
        return response


class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerCreateForm
    success_url = '/app/owner/list'
    template_name = 'app/owner_create.html'
    permission_required = 'app.add_owner'

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    model = Owner
    fields = ['last_name', 'first_name', 'birth_date']
    success_url = '/app/owner/list'
    template_name = 'app/owner_update.html'
    permission_required = 'app.change_owner'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Owner updated successfully!")
        return response


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    model = Owner
    success_url = '/app/owner/list'
    template_name = 'app/owner_delete.html'
    permission_required = 'app.delete_owner'

    def delete(self, request, *args, **kwargs):
        owner = self.get_object()
        user_to_delete = owner.user
        response = super().delete(request, *args, **kwargs)
        user_to_delete.delete()
        messages.success(request, "Owner and associated user deleted successfully!")
        return response

class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'app/register.html'
    success_message = "User registered successfully!"

# тут отдельная функция для избежания редиректа
def user_create_modal(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "User created successfully!")
        return redirect('owner_list')
    else:
        messages.error(request, "There was an error in the form. Please check the input.")
        return redirect('owner_list')

@login_required
def home(request):
    if request.user.is_superuser:
        role = "Admin"
    else:
        role = "User"
    return render(request, 'app/home.html', {'role': role})

@login_required
def rentals_view(request):
    owner = get_object_or_404(Owner, user=request.user)

    current_date = now().date()

    current_rentals = CarOwner.objects.filter(owner_id=owner, date_end__gt=current_date)

    past_rentals = CarOwner.objects.filter(owner_id=owner, date_end__lte=current_date)

    return render(request, 'app/rentals.html', {
        'current_rentals': current_rentals,
        'past_rentals': past_rentals,
    })

@login_required
def end_rental(request, rental_id):

    print(rental_id)

    rental = get_object_or_404(CarOwner, id=rental_id, owner_id__user=request.user)

    current_date = now().date()

    if rental.date_end and rental.date_end <= current_date:
        raise Http404("This rental has already ended or cannot be modified.")

    rental.date_end = current_date
    rental.save()

    return redirect('rentals')


@login_required
def available_cars(request):
    rented_cars = CarOwner.objects.filter(date_end__gt=now()).values_list('car_id', flat=True)

    available_cars = Car.objects.exclude(id__in=rented_cars)

    return render(request, 'app/available_cars.html', {'available_cars': available_cars})

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'app/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

@login_required
def role_redirect(request):
    if request.user.is_superuser:
        return redirect('home_admin')
    return redirect('home_user')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    return render(request, 'app/home_admin.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_rentals(request):
    current_date = now().date()
    occupied_cars = CarOwner.objects.filter(date_end__gte=current_date).values_list('car_id', flat=True)
    available_cars = Car.objects.exclude(id__in=occupied_cars)
    owners = Owner.objects.exclude(first_name__isnull=True).exclude(first_name="").exclude(last_name__isnull=True).exclude(last_name="")
    rentals = CarOwner.objects.all()
    return render(request, 'app/manage_rentals.html', {
        'rentals': rentals,
        'cars': available_cars,
        'owners': owners,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_rental(request, rental_id):
    rental = get_object_or_404(CarOwner, id=rental_id)
    if request.method == 'POST':
        form = CarOwnerForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rental updated successfully!')
        else:
            messages.error(request, 'Failed to update rental. Please check the form.')
    return redirect('manage_rentals')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_rental(request, rental_id):
    rental = get_object_or_404(CarOwner, id=rental_id)
    rental.delete()
    messages.success(request, 'Rental deleted successfully!')
    return redirect('manage_rentals')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_rental(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        owner_id = request.POST.get('owner_id')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')

        if not all([car_id, owner_id, date_start, date_end]):
            messages.error(request, "Please fill in all required fields!")
            return redirect('manage_rentals')

        current_date = now().date()
        occupied_cars = CarOwner.objects.filter(date_end__gte=current_date).values_list('car_id', flat=True)

        if int(car_id) in occupied_cars:
            messages.error(request, "This car is not available!")
            return redirect('manage_rentals')

        CarOwner.objects.create(
            car_id_id=car_id,
            owner_id_id=owner_id,
            date_start=date_start,
            date_end=date_end
        )
        messages.success(request, "Rental created successfully!")
        return redirect('manage_rentals')

    return redirect('manage_rentals')