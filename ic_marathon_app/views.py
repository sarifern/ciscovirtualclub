from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile, Workout, WorkoutForm
from badgify.models import Award, Badge
from django.shortcuts import redirect

# TODO[sarifern] document every function

# Create your views here.


def login(request):
    return render(request, 'registration/login.html')


@login_required
def home(request):
    if request.user.profile.cec:
        return my_workouts(request)
    else:
        return profile_wizard(request)


@login_required
def my_workouts(request):
    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile)
    except ObjectDoesNotExist:
        workouts = {}
    return render(request, 'ic_marathon_app/my_workouts.html', {'workouts': workouts})


@login_required
def add_workout(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST, request.FILES)
        form.instance.belongs_to = request.user.profile
        if form.is_valid():
            form.save()
            new_badge = check_badges(request.user)
            if new_badge:
                return render(request, 'ic_marathon_app/add_workout.html', {'form': form, 'new_badge': new_badge})
            else:
                return redirect('home')
        else:
            return render(request, 'ic_marathon_app/add_workout.html', {'form': form})
    else:
        form = WorkoutForm()
        return render(request, 'ic_marathon_app/add_workout.html', {'form': form})


@login_required
def leaderboard(request):
    return render(request, 'ic_marathon_app/leaderboard.html')


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
    profile = user.profile
    distance = user.profile.distance

    if distance >= 168.0:
        return award_badge(user=user, slug='168K')
    elif profile.distance >= 126.0:
        return award_badge(user=user, slug='126K')
    elif profile.distance >= 84.0:
        return award_badge(user=user, slug='84K')
    elif profile.distance >= 80.0 and profile.category == "beginnerrunner":
        profile.category = "runner"
        profile.save()
    elif profile.distance >= 42.0:
        return award_badge(user=user, slug='42K')
    elif profile.distance >= 21.0:
        return award_badge(user=user, slug='21K')
    elif profile.distance >= 10.0:
        return award_badge(user=user, slug='10K')

    return None


def award_badge(user, slug):
    new_badge = Badge.objects.get(slug=slug)
    obj, created = Award.objects.get_or_create(
        user=user, badge=new_badge)
    if created:
        return new_badge
    else:
        return None
