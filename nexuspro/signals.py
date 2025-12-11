from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile # Import your Profile model

# ----------------------------------------------------------------------
# Signal 1: Create Profile when a new User is saved
# ----------------------------------------------------------------------

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Called after a User instance is saved.
    If a new user was created (created=True), a Profile object is also created.
    """
    if created:
        # Create a new Profile instance linked to the newly created User
        Profile.objects.create(user=instance)

# ----------------------------------------------------------------------
# Signal 2: Save Profile when the User is saved (used for profile editing)
# ----------------------------------------------------------------------

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Called after a User instance is saved (during profile editing).
    Ensures the corresponding Profile is also saved.
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Handle cases where profile might be missing (e.g., initial migration, though Signal 1 should prevent this)
        # We can safely pass here as Signal 1 handles creation if 'created' is True
        pass