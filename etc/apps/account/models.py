from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


def get_default_image():
    return 'image_profiles/default/default.jpg'

class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE,
                                      related_name='profile')
    full_name  = models.CharField(max_length=70)
    image      = models.ImageField('Image',
                                   upload_to='image_profiles', default=get_default_image)
    phone      = models.CharField(max_length=30)
    friends    = models.ManyToManyField("self", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name}, {self.phone}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()
