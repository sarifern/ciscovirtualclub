from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage
from django.forms import ModelForm
from django.dispatch import receiver
import uuid
from .validators import validate_file_size, validate_workout_time, validate_team_members
import q
# Create your models here.


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_goal = models.BooleanField(default=False)

    def __str__(self):
        return self.team_name


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=200, blank=False)
    user_goal = models.BooleanField(default=False)
    cec = models.CharField(max_length=30, blank=True)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)
    RUNNER = "Runner"
    BIKER = "Biker"
    CATEGORY_CHOICES = (
        (None, 'Please select a category'),
        (RUNNER, 'Runner'),
        (BIKER, 'Biker'),
    )
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, blank=True, null=True)
    team = models.ForeignKey(
        Team, related_name="related_team", default=None, on_delete=models.CASCADE, blank=True, null=True, validators=[
            validate_team_members])

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
    if profile.distance >= 42.0:
        profile.user_goal = True
    else:
        profile.user_goal = False
    profile.save()

    # delete image from S3
    try:
        default_storage.delete(instance.photo_evidence.name)
    except Exception:
        q("Can't delete the file {} in S3".format(instance.photo_evidence.name))

    # update team goal
    team = profile.team
    profiles = Profile.objects.filter(team__team_name=team.team_name)
    team_goal = True
    for profile in profiles:
        if not profile.user_goal:
            team_goal = False
            break

    if team_goal:
        team.team_goal = True
    else:
        team.team_goal = False
    team.save()


@receiver(post_save, sender=Workout)
def save_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance += instance.distance
    if profile.distance >= 42.0:
        profile.user_goal = True
    profile.save()

    # update team goal
    team = profile.team
    profiles = Profile.objects.filter(team__team_name=team.team_name)
    team_goal = True
    for profile in profiles:
        if not profile.user_goal:
            team_goal = False
            break

    if team_goal:
        team.team_goal = True
    team.save()
