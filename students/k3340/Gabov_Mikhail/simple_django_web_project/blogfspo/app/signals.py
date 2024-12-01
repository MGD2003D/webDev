from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Owner

@receiver(post_save, sender=User)
def create_owner_for_user(sender, instance, created, **kwargs):
    if created:  # Только при создании нового пользователя
        Owner.objects.create(
            first_name=instance.first_name,
            last_name=instance.last_name,
            birth_date=instance.birth_date,
            user=instance  # Связь с пользователем
        )