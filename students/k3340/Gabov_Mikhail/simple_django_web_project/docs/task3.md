# Практическая работа 2.3

## Расширение пользовательской модели

Создание новой модели пользователя, унаследованной от `AbstractUser`

```py 
class User(AbstractUser):
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
```

Представление `views.py`

```py 
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name', 'passport_number', 'address', 'nationality']
    template_name = 'baseuser_create.html'
    success_url = '/app/owner/list'
```

Объявление модели в `settings.py`
```py 
AUTH_USER_MODEL = 'app.User'
```

Отображение в админ панели `admin.py`
```py 
@admin.register(User)
class BaseUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('passport_number', 'address', 'nationality'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'address', 'nationality', 'is_active', 'is_staff', 'is_superuser')
```

## Соответствие Owner и User

*Регистрируясь, пользователь получает доступ к управлению владельцем, соответствующим ему и созданным при его регистрации*

Сигнал для автоматического создания `Owner` в `app/signals.py`
```py 
@receiver(post_save, sender=User)
def create_owner_for_user(sender, instance, created, **kwargs):
    if created:  # Только при создании нового пользователя
        Owner.objects.create(
            first_name=instance.first_name,
            last_name=instance.last_name,
            birth_date=instance.birth_date,
            user=instance  # Связь с пользователем
        )
```

Регистрация сигнала в `apps.py`
```py 
from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from . import signals
```

Обновленные `Owner` и `User`
```py 
class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True)
    cars = models.ManyToManyField('Car', through='CarOwner')

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
```

Представление для создания пользователя
```py 
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'app/register.html'
```

Форма
```py 
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'passport_number',
            'address',
            'nationality',
            'birth_date',
        ]
```

Маршрут
```py 
path('register/', UserCreateView.as_view(), name='user_create')
```

## Ограничение прав пользователя

Пример для отображения владельцу только его аренд
```py 
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
```


Для авторизации используется `django.contrib.auth.urls`
```py 
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
```

`django.contrib.messages` — для отображения `Toast` скриптов

только сейчас я узнал про base.html ... можно было не делать всем шапки по отдельности!