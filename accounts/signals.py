from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from .models import Balance


@receiver(post_save, sender=CustomUser)
def post_save_balance(sender, instance: CustomUser, created, **kwargs):
    if created:
        balance = Balance.objects.create(user=sender)