from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage
from django.forms import ModelForm
from django import forms
from django.dispatch import receiver
from django_select2.forms import Select2Widget
import uuid
from .validators import validate_file_size, validate_workout_time 
import q

# Create your models here.
BABYRUNNER = "babyrunner"
RUNNER = "runner"
BIKER = "biker"

CATEGORY_CHOICES = (
    (BABYRUNNER, 'Baby Runner'),
    (RUNNER, 'Runner'),
    (BIKER, 'Biker'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=200, blank=False)
    user_goal = models.BooleanField(default=False)
    cec = models.CharField(max_length=30, blank=True)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)

    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES,blank=False,default=BABYRUNNER)

    def check_achievements(self,distance):
        if distance >= 70.0 and self.category=="babyrunner":
            self.category = "runner"
        elif distance < 42.0:
            self.user_goal = False
        elif distance >= 42.0:
            self.user_goal = True

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
    belongs_to = models.OneToOneField(
        Profile, on_delete=models.CASCADE, default=None)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)
    photo_evidence = models.ImageField(validators=[validate_file_size])
    time = models.IntegerField(help_text='Workout in minutes', validators=[
                               validate_workout_time])


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['distance', 'photo_evidence', 'time']


@receiver(post_delete, sender=Workout)
def delete_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance -= instance.distance
    profile.check_achievements(profile.distance)
    profile.save()

    # delete image from S3
    try:
        default_storage.delete(instance.photo_evidence.name)
    except Exception:
        q("Can't delete the file {} in S3".format(instance.photo_evidence.name))


@receiver(post_save, sender=Workout)
def save_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance += instance.distance
    profile.check_achievements(profile.distance)
    profile.save()
