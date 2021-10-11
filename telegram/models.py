from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TeleGroup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True, related_name='owner')
    follower = models.ManyToManyField(User, blank=True, related_name='follower')
    number_followers = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def connect_owner(self, request):
        self.owner = request.user
        self.save()

    def add_user(self, request):
        if not self.follower.filter(pk=request.user.pk).exists():
            self.follower.add(request.user)
            self.number_followers += 1
            self.save()
            return True


class Message(models.Model):
    user = models.ForeignKey(User, blank=True, related_name='user', on_delete=models.CASCADE)
    group = models.ForeignKey(TeleGroup, blank=True, related_name='group', on_delete=models.CASCADE)
    value = models.TextField()
    date_send = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.group} - {self.user} - {self.value[:10]}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=120, null=True)
    phone = models.CharField(max_length=120, null=True, default='')
    email = models.CharField(max_length=120, null=True)
    photo = models.ImageField(default='default.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance, email=instance.email, username=instance.username)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def __str__(self):
        return f"Profile of User: {self.user.username}"
