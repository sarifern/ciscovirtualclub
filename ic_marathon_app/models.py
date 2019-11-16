from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import ModelForm
from django import forms
from django.dispatch import receiver
from django_select2.forms import Select2Widget
import uuid
from badgify.models import Award, Badge
import q

# Create your models here.
BEGINNERRUNNER = "beginnerrunner"
RUNNER = "runner"
BIKER = "biker"

CATEGORY_CHOICES = (
    (BEGINNERRUNNER, 'Beginner Runner'),
    (RUNNER, 'Runner'),
    (BIKER, 'Biker'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    avatar = models.CharField(max_length=200, blank=False)
    cec = models.CharField(max_length=30, blank=True)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)

    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, blank=False, default=BEGINNERRUNNER)


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['cec', 'category']


'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.username != "lurifern":
        instance.profile.save()
'''


class Workout(models.Model):
    belongs_to = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, unique=False)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)
    photo_evidence = models.ImageField()
    time = models.IntegerField(help_text='Workout in minutes')


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['distance', 'photo_evidence', 'time']


"""
@receiver(post_delete, sender=Workout)
def delete_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance -= instance.distance
    # TODO probably a badge
    profile.save()

    # delete image from S3
    try:
        default_storage.delete(instance.photo_evidence.name)
    except Exception:
        q("Can't delete the file {} in S3".format(instance.photo_evidence.name))
"""


@receiver(post_save, sender=Workout)
def save_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance += instance.distance
    # TODO check possible badge
    check_badges(profile, profile.distance)
    profile.save()


def check_badges(profile, distance):

    user = profile.user
    if distance >= 168.0:
        Award.objects.create(user=user, badge=Badge.objects.get(slug='168K'))
    elif profile.distance >= 126.0:
        Award.objects.create(
            user=user, badge=Badge.objects.get(slug='126K'))
    elif profile.distance >= 84.0:
        Award.objects.create(
            user=user, badge=Badge.objects.get(slug='84K'))

    elif profile.distance >= 42.0:
        Award.objects.create(
            user=user, badge=Badge.objects.get(slug='42K'))
        profile.user_goal = True
        profile.save()
    elif profile.distance >= 21.0:
        Award.objects.create(
            user=user, badge=Badge.objects.get(slug='21K'))
    elif profile.distance >= 10.0:
        Award.objects.create(
            user=user, badge=Badge.objects.get(slug='10K'))
