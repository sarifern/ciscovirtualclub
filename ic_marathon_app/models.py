from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage
from ic_marathon_site.storage_backends import PrivateMediaStorage
from django.forms import ModelForm
from django import forms
from django.dispatch import receiver
from django_select2.forms import Select2Widget
from bootstrap_datepicker_plus import TimePickerInput, DateTimePickerInput
import uuid
from .validators import validate_file_size, validate_workout_time, validate_distance, validate_date
import q
from badgify.models import Award, Badge
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import ApiError
import os
# Create your models here.
WTAPI = WebexTeamsAPI(access_token=os.environ.get('WT_TOKEN'))
RUNNER = "runner"

CATEGORY_CHOICES = ((RUNNER, 'Runner'), )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_donated = models.BooleanField(default=False)
    avatar = models.CharField(max_length=400, blank=False)
    email = models.CharField(max_length=30, blank=True)
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=RUNNER)

    def __str__(self):
        return self.email


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['email']


#Expand the model for the special WorkoutForm (free style)
class Workout(models.Model):
    belongs_to = models.ForeignKey(Profile,
                                   on_delete=models.CASCADE,
                                   default=None,
                                   unique=False)
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    date_time = models.DateTimeField(verbose_name="Date",
                                     validators=[validate_date])



class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['distance', 'date_time']
        widgets = {
            'date_time': DateTimePickerInput(),
        }




@receiver(post_delete, sender=Workout)
def delete_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance -= instance.distance

    profile.save()

@receiver(post_save, sender=Profile)
def save_profile(sender, instance, **kwargs):
    # update personal distance
    if instance.has_donated:
        imagegif = 'https://media.giphy.com/media/LUPCYuP1GjmcF9tOL9/giphy.gif'
        try:
            WTAPI.messages.create(
                roomId=os.environ.get('WT_ROOMID'),
                text='Thank you so much! {username}  #Giveback Ambassador'.format(username=instance.user.first_name),
                files=[imagegif])
        except Exception:
            pass

@receiver(post_save, sender=Workout)
def save_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance += instance.distance
    profile.save()
    user = User.objects.get(profile=profile)
    new_badges,imagegif = check_badges(user)
    if new_badges:
        try:
            WTAPI.messages.create(
                roomId=os.environ.get('WT_ROOMID'),
                text=new_badges[-1].description.format(username=user.first_name),
                files=[imagegif])
        except Exception:
            pass
    

def check_badges(user):
    """Check awarded badges for each user

    Arguments:
        user {User} -- Session user

    Returns:
        new_badges {[Award]} -- list of Award objects
    """
    distance = user.profile.distance
    new_badges = []
    imagegif=""
    if distance >= 5.0:
        new_badge = award_badge(user=user, slug='5K')
        if new_badge:
            new_badges.append(new_badge)
            imagegif = 'https://media.giphy.com/media/007kAUpYBOw1XxOjhX/giphy.gif'
    if distance >= 10.0:
        new_badge = award_badge(user=user, slug='10K')
        if new_badge:
            new_badges.append(new_badge)
            imagegif = 'https://media.giphy.com/media/xzBRnDRffHPerqTYs7/giphy.gif'
    if distance >= 15.0:
        new_badge = award_badge(user=user, slug='15K')
        if new_badge:
            new_badges.append(new_badge)
            imagegif = 'https://media.giphy.com/media/aFObuJMBFeSsLWdr88/giphy.gif'
    if distance >= 21.0:
        new_badge = award_badge(user=user, slug='21K')
        if new_badge:
            new_badges.append(new_badge)
            imagegif = 'https://media.giphy.com/media/Tqk01KcKQACjiPqSj4/giphy.gif'
    if distance >= 30.0:
        new_badge = award_badge(user=user, slug='30K')
        if new_badge:
            new_badges.append(new_badge)
            imagegif='https://media.giphy.com/media/k15VLa8YnA5bYZU01H/giphy.gif'
    if distance >= 42.0:
        new_badge = award_badge(user=user, slug='42K')
        if new_badge:
            new_badges.append(new_badge)
            imagegif='https://media.giphy.com/media/NHUUjBOPQEZIplDWGo/giphy.gif'

    return new_badges,imagegif


def strip_badges(user):
    """Strip badges if workouts are deleted (if applicable)

    Arguments:
        user {User} -- Session User
    """
    distance = user.profile.distance
    if distance < 42.0 and get_award(user, slug='42K'):
        get_award(user, slug='42K').delete()
    if distance < 30.0 and get_award(user, slug='30K'):
        get_award(user, slug='30K').delete()
    if distance < 21.0 and get_award(user, slug='21K'):
        get_award(user, slug='21K').delete()
    if distance < 15.0 and get_award(user, slug='15K'):
        get_award(user, slug='15K').delete()
    if distance < 10.0 and get_award(user, slug='10K'):
        get_award(user, slug='10K').delete()
    if distance < 5.0 and get_award(user, slug='5K'):
        get_award(user, slug='5K').delete()


def award_badge(user, slug):
    """Award new badge if applicable

    Arguments:
        user {User} -- Request User
        slug {string} -- Unique slug for each badge

    Returns:
        new_badge -- New Award for the User, if it is created return new_badge, if not return None
    """
    new_badge = Badge.objects.get(slug=slug)
    obj, created = Award.objects.get_or_create(user=user, badge=new_badge)
    if created:
        return new_badge
    else:
        return None


def get_award(user, slug):
    """Get awarded badge for user and unique slug

    Arguments:
        user {Request} -- Session user
        slug {string} -- Unique slug name of Badge

    Returns:
        award -- Award if found, if not return None
    """
    try:
        old_badge = Badge.objects.get(slug=slug)
        return Award.objects.get(user=user, badge=old_badge)
    except:
        # Award not granted
        return None