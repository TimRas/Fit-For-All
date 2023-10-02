from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_delivery_address = models.CharField(max_length=255)
    order_history = models.ManyToManyField('Order', blank=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    # Add other fields related to the order, such as products, quantities, etc.

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

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
        instance.userprofile.save()

# Connect the signal to the User model
post_save.connect(create_or_update_user_profile, sender=User)
