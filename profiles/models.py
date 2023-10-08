from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create or update a user profile
    when a new user is created or an existing user is saved.
    """
    if created:
        # If a new user is created, create a corresponding user profile.
        UserProfile.objects.create(user=instance)
    else:
        # If an existing user is saved, update their user profile.
        profile, _ = UserProfile.objects.get_or_create(user=instance)


# # Connect the signal to the User model
post_save.connect(create_or_update_user_profile, sender=User)

