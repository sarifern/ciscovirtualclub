"""ic_marathon_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ic_marathon_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.login, name="login"),
    path("profile_wizard/", views.profile_wizard, name="profile_wizard"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(r'^complete/(?P<backend>[^/]+)/$', views.complete, name='complete'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("", views.home, name="home"),
    path('select2/', include('django_select2.urls')),
    path('badges/',include('badgify.urls')),
]
