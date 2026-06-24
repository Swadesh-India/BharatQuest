from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from .utils import generate_initials_avatar 
@receiver(post_save, sender=User)
def create_user_profile_and_avatar(sender, instance, created, **kwargs):
    """
    'created' is a boolean that is True only when a new record is created.
    'instance' is the actual User object that was just saved.
    """
    if created:
        Profile.objects.create(user=instance)
        generate_initials_avatar(instance)
    if hasattr(instance, 'profile'):
        instance.profile.save()

