from social_django.views import _do_login
from social_core.actions import do_auth, do_complete, do_disconnect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile, Workout, WorkoutForm
from badgify.models import Award, Badge
from django.shortcuts import redirect, render, get_object_or_404
from .tables import WorkoutTable, ProfileTable
from datetime import datetime
from django_tables2.config import RequestConfig
from django_tables2.paginators import LazyPaginator
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import ApiError
from decimal import *
import itertools
import os
import pytz as tz

WTAPI = WebexTeamsAPI(access_token=os.environ.get('WT_TOKEN'))



# Create your views here.


def login(request):
    """Login view, implements Django Auth Package

    Arguments:
        request {Request} -- Request from the browser.

    Returns:
        rendered template -- Rendered template depending on successful or failed auth.
    """
    return render(request, 'registration/login.html')


@login_required
def home(request):
    if request.user.profile.email:
        return leaderboard(request)
    else:
        return profile_wizard(request)


@login_required
def my_profile(request):
    """Returns My Profile information (workouts, distance, remaining days from the Marathon, current position
    in leaderboard)

    Arguments:
        request {Request} -- Request from browser

    Returns:
        rendered template -- Rendered template (my_profile.html) with Profile information as dict
        variables
        {
        'earned_awards': awards,

        'position': position,
        'workout_count': len(workouts),
        'aggr_distance': request.user.profile.distance,
        
        }
    """
    # need workouts count, distance count, remaining days
    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile)
        awards = Award.objects.filter(user=request.user)
        list_in_category = Profile.objects.filter(
            category=request.user.profile.category).order_by('-distance')
        list_cec_in_category = list(existing_profile
                                    for existing_profile in list_in_category)
        index = list_cec_in_category.index(request.user.profile) + 1

    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
    return render(
        request, 'ic_marathon_app/my_profile.html', {
            'earned_awards': awards,
            'position': index,
            'workout_count': len(workouts),
            'aggr_distance': request.user.profile.distance,
            'aggr_distance_per': int(
                (request.user.profile.distance / 168) * 100),
           
        })



@login_required
def leaderboard(request):
    """View to handle the Delete Workout form

    Arguments:
        request {Request} -- The Request from the browser

    Returns:
        rendered template -- Rendered templates with 3 tables (sorted by descending distance)
    """
    try:
        earned_awards = Award.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        earned_awards = {}
    leaders_r = Profile.objects.filter(category="runner").order_by('-distance')
    

    total_workouts = Workout.objects.all()
    total_kms = 0
    for workout in total_workouts:
        total_kms += workout.distance
    table_leaders_r = ProfileTable(leaders_r, prefix="leaders-r-")
    
    RequestConfig(request, paginate={
        "per_page": 10
    }).configure(table_leaders_r)
    

    return render(
        request, 'ic_marathon_app/leaderboard.html', {
            'leaders_r': table_leaders_r,
            'leaders_r_c': len(leaders_r),
            'earned_awards': earned_awards,
            'total_kms': total_kms
        })



@login_required
def profile_wizard(request):
    """View to fill Profile form

    Arguments:
        request {Request} -- The Request from the browser

    Returns:
        rendered template -- Render to My workouts, with modal for successful activation
    """
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            wtFlag = False
            try:
                WTAPI.memberships.create(roomId=os.environ.get('WT_ROOMID'),
                                         personEmail=profile.email,
                                         isModerator=False)
                WTAPI.messages.create(
                    roomId=os.environ.get('WT_ROOMID'),
                    text="Let's welcome " + request.user.first_name + " (" +
                    profile.email + ") to the challenge! \nGive your best!",
                    markdown=None)
            except ApiError:
                wtFlag = True
            return render(request, 'ic_marathon_app/profile_wizard.html', {
                'form': form,
                'activation': True,
                'wtFlag': wtFlag
            })
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'ic_marathon_app/profile_wizard.html', {
        'form': form,
    })


def check_badges(user):
    """Check awarded badges for each user

    Arguments:
        user {User} -- Session user

    Returns:
        new_badges {[Award]} -- list of Award objects
    """
    distance = user.profile.distance
    new_badges = []
    if distance >= 5.0:
        new_badge = award_badge(user=user, slug='5K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 10.0:
        new_badge = award_badge(user=user, slug='10K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 15.0:
        new_badge = award_badge(user=user, slug='15K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 21.0:
        new_badge = award_badge(user=user, slug='21K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 30.0:
        new_badge = award_badge(user=user, slug='30K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 42.0:
        new_badge = award_badge(user=user, slug='42K')
        if new_badge:
            new_badges.append(new_badge)

    return new_badges


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


NAMESPACE = 'social'
REDIRECT_FIELD_NAME = 'next'


def complete(request, backend, *args, **kwargs):
    """Authentication complete view OVERRIDE

    Arguments:
        request {Request} -- Request from Browser
        backend {string} -- Authentication Backend

    """
    return do_complete(request.backend,
                       _do_login,
                       user=None,
                       redirect_name=REDIRECT_FIELD_NAME,
                       request=request,
                       *args,
                       **kwargs)


def float_to_decimal(f):
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[Inexact]:
        ctx.flags[Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result