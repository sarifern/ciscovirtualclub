from social_django.views import _do_login
from social_core.actions import do_auth, do_complete, do_disconnect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile, Workout, WorkoutForm
from badgify.models import Award, Badge
from django.shortcuts import redirect, render, get_object_or_404
from .tables import WorkoutTable, ProfileTable
from datetime import datetime
# TODO CHANGE when pushing to github
ENV = "PROD"

# TODO[sarifern] document every function

# Create your views here.
DATE_START = datetime(2019, 12, 12, 0, 0, 0)
DATE_END = datetime(2020, 1, 7, 0, 0, 0)

if ENV == "STAGE":
    DATE = datetime(2019, 12, 14, 0, 0, 0)
else:
    DATE = datetime.now()
# Check time period DIC 12 to Jan 6
if DATE >= DATE_START and DATE <= DATE_END:
    ACTIVE = True
else:
    ACTIVE = False


def login(request):
    return render(request, 'registration/login.html')


@login_required
def home(request):
    if request.user.profile.cec:
        return my_workouts(request)
    else:
        return profile_wizard(request)


@login_required
def my_profile(request):
    # need workouts count, distance count, remaining days
    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile)
        awards = Award.objects.filter(user=request.user)
        remaining_days = DATE_END-DATE
    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
    return render(request, 'ic_marathon_app/my_profile.html', {
        'awards': awards,
        'active': ACTIVE,
        'workout_count': len(workouts),
        'aggr_distance': request.user.profile.distance,
        'remaining_days_per': int(((remaining_days.days)/26)*100),
        'remaining_days': remaining_days.days})


@login_required
def my_workouts(request):

    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile)
        workouts_table = WorkoutTable(workouts)

        awards = Award.objects.filter(user=request.user)

    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
    return render(request, 'ic_marathon_app/my_workouts.html', {'workouts': workouts_table,
                                                                'awards': awards,
                                                                'active': ACTIVE,
                                                                'ENV': ENV,
                                                                'workout_count': len(workouts),
                                                                'aggr_distance': request.user.profile.distance,
                                                                })


@login_required
def add_workout(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST, request.FILES)
        form.instance.belongs_to = request.user.profile
        if form.is_valid():
            form.save()
            new_badges = check_badges(request.user)
            if new_badges:
                return render(request, 'ic_marathon_app/add_workout.html', {'form': form, 'new_badges': new_badges})
            else:
                return redirect('home')
        else:
            return render(request, 'ic_marathon_app/add_workout.html', {'form': form})
    else:
        form = WorkoutForm()
        return render(request, 'ic_marathon_app/add_workout.html', {'form': form})


@login_required
def delete_workout(request, uuid):
    if uuid:
        workout = get_object_or_404(Workout, uuid=uuid)
        workout.delete()
        request.user.profile.save()
        strip_badges(request.user)
        return redirect('home')


@login_required
def leaderboard(request):
    leaders_br = Profile.objects.filter(
        category="beginnerrunner").order_by('-distance')
    leaders_r = Profile.objects.filter(category="runner").order_by('-distance')
    leaders_b = Profile.objects.filter(category="biker").order_by('-distance')
    return render(request, 'ic_marathon_app/leaderboard.html',
                  {'leaders_br': ProfileTable(leaders_br), 'leaders_r': ProfileTable(leaders_r),
                   'leaders_b': ProfileTable(leaders_b)})


@login_required
def profile_wizard(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'ic_marathon_app/profile_wizard.html', {'form': form, 'activation': True})
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'ic_marathon_app/profile_wizard.html', {'form': form})


def check_badges(user):
    distance = user.profile.distance
    new_badges = []
    if distance >= 168.0:
        new_badge = award_badge(user=user, slug='168K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 126.0:
        new_badge = award_badge(user=user, slug='126K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 84.0:
        new_badge = award_badge(user=user, slug='84K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 42.0:
        new_badge = award_badge(user=user, slug='42K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 21.0:
        new_badge = award_badge(user=user, slug='21K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 10.0:
        new_badge = award_badge(user=user, slug='10K')
        if new_badge:
            new_badges.append(new_badge)

    return new_badges


def strip_badges(user):
    """
    Strip badges if workouts are deleted (if applicable)
    """
    distance = user.profile.distance
    if distance < 168.0 and get_award(user, slug='168K'):
        get_award(user, slug='168K').delete()
    if distance < 126.0 and get_award(user, slug='126K'):
        get_award(user, slug='126K').delete()
    if distance < 84.0 and get_award(user, slug='84K'):
        get_award(user, slug='84K').delete()
    if distance < 42.0 and get_award(user, slug='42K'):
        get_award(user, slug='42K').delete()
    if distance < 21.0 and get_award(user, slug='21K'):
        get_award(user, slug='21K').delete()
    if distance < 10.0 and get_award(user, slug='10K'):
        get_award(user, slug='10K').delete()


def award_badge(user, slug):
    new_badge = Badge.objects.get(slug=slug)
    obj, created = Award.objects.get_or_create(
        user=user, badge=new_badge)
    if created:
        return new_badge
    else:
        return None


def get_award(user, slug):
    try:
        old_badge = Badge.objects.get(slug=slug)
        return Award.objects.get(user=user, badge=old_badge)
    except:
        # Award not granted
        return None


NAMESPACE = 'social'
REDIRECT_FIELD_NAME = 'next'


def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    return do_complete(request.backend, _do_login, user=None,
                       redirect_name=REDIRECT_FIELD_NAME, request=request,
                       *args, **kwargs)
