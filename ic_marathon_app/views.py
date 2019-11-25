from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile, Workout, WorkoutForm
from badgify.models import Award, Badge
from django.shortcuts import redirect
from .tables import WorkoutTable, ProfileTable
from datetime import datetime
# TODO[sarifern] document every function

# Create your views here.
DATE_START = datetime(2019, 12, 12, 0, 0, 0)
DATE_END = datetime(2020, 1, 7, 0, 0, 0)


def login(request):
    return render(request, 'registration/login.html')


@login_required
def home(request):
    date = datetime.now()
    # Check time period DIC 12 to Jan 6
    if date >= DATE_START and date <= DATE_END:
        active = True
    else:
        active = False

    if request.user.profile.cec:
        return my_workouts(request, active)
    else:
        return profile_wizard(request)


@login_required
def my_workouts(request, active=False):
    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile)
        workouts_table = WorkoutTable(workouts)

        awards = Award.objects.filter(user=request.user)

    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
    return render(request, 'ic_marathon_app/my_workouts.html', {'workouts': workouts_table,
                                                                'awards': awards,
                                                                'active': active})


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
def leaderboard(request):
    leaders_br = Profile.objects.filter(
        category="beginnerrunner").order_by('distance')
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
            return redirect('home')
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


def award_badge(user, slug):
    new_badge = Badge.objects.get(slug=slug)
    obj, created = Award.objects.get_or_create(
        user=user, badge=new_badge)
    if created:
        return new_badge
    else:
        return None
