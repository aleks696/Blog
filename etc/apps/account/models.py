from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE,
                                      related_name='profile')
    full_name  = models.CharField(max_length=70)
    image      = models.ImageField('Image',
                                   upload_to='image_profiles', default='image_profiles/default/default.jpg')
    phone      = models.CharField(max_length=30)
    friends    = models.ManyToManyField("self", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name}, {self.phone}'

    def add_friend(self, profile):
        if not profile in self.friends.all():
            self.friends.add(profile)
            self.save()

    def remove_friend(self, profile):
        if profile in self.friends.all():
            self.friends.remove(profile)

    def unfollow_friend(self, remover):
        remover_friends_list = self
        remover_friends_list.remove_friend(remover)
        friends_list = Profile.objects.get(user=remover)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend is self.friends.all():
            return True
        return False

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()


class FriendRequest(models.Model):
    """ Different types of requests to users """
    sender = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """ Accept friend request """
        receiver_profile = Profile.objects.get(user=self.receiver)
        sender_profile = Profile.objects.get(user=self.sender)
        if receiver_profile and sender_profile:
            receiver_profile.add_friend(self.sender)
            sender_profile.add_friend(self.receiver)
            self.is_active = False
            self.save()

    def decline(self):
        """ Decline a friend request """
        self.is_active = False
        self.save()

    def cancel(self):
        """ Cancel a friend request """
        self.is_active = False
        self.save()
