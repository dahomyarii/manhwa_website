from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Import the User model
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):  # Check if the user has a related userprofile
        instance.userprofile.save()
