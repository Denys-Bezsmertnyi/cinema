from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=Token)
def token_post_save(sender, instance, created, **kwargs):
    if created:
        expiration_time = timezone.now() + timezone.timedelta(seconds=5)
        instance.created = expiration_time
        instance.save()
