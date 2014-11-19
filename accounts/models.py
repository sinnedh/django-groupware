from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile_for_user(sender, instance=None, created=False, **kwargs):
        if created:
            UserProfile.objects.get_or_create(user=instance)

    @receiver(pre_delete, sender=User)
    def delete_profile_for_user(sender, instance=None, **kwargs):
        if instance:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.delete()
