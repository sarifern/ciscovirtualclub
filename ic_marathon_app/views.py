from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile, Workout, WorkoutForm
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

    # TODO[sarifern] put the POST functionality
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
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
