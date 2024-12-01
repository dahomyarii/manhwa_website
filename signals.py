from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """Create or save UserProfile when a User is created or updated."""
    profile, created = UserProfile.objects.get_or_create(user=instance)
    if not created:  # Save the profile if it already exists
        profile.save()
