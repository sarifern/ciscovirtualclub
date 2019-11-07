from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile
from django.shortcuts import redirect

# Create your views here.


def login(request):
    return render(request, 'registration/login.html')


@login_required
def home(request):
    return render(request, 'ic_marathon_app/home.html')


@login_required
def profile_wizard(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'ic_marathon_app/profile_wizard.html', {'form': form})
