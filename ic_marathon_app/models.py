from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .validators import validate_file_size
# Create your models here.


class Workout(models.Model):
    belongs_to = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, default=None)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)
    photo_evidence = models.ImageField(validators=[validate_file_size])


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)

    def __str__(self):
        return self.team_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cec = models.CharField(max_length=30)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)
    RUNNER = "Runner"
    BIKER = "Biker"
    CATEGORY_CHOICES = (
        (None, 'Please select a category'),
        (RUNNER, 'Runner'),
        (BIKER, 'Biker'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    team = models.OneToOneField(
        Team, related_name="team", default=None, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
