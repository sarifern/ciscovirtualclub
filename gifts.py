from ic_marathon_app.models import Profile
from django.core.exceptions import MultipleObjectsReturned
from ic_marathon_app.views import check_badges

cecs_who_joined = [
    "sromerob",
    "joalamo",
    "gzepedag",
    "flugo",
    "lguzmanp",
    "albenit",
    "dianaro",
    "sanespin",
    "bguerram",
    "anaarand",
    "jmauleon",
    "dleconac",
    "yohomma",
    "fabherna",
    "rdelaveg",
    "antjuare",
    "jgandari",
    "cecilmar",
    "maespond",
    "fabporra",
    "igalanva",
    "criveras",
    "osuarezp",
    "dalbanil",
    "learroyo",
    "ivillega",
    "yramales",
    "guigarci",
    "alesalga",
    "edusanc2",
    "gtomich",
    "ellopeza",
    "eribyrne",
    "daniesan",
    "marintor",
    "juaferna",
    "gesantia",
    "pofarril",
    "artmoral",
    "jcraviot",
    "edfonsec",
    "victogut",
    "alejanme",
    "lramosba",
    "arojaslo",
    "emejiame",
    "lparra",
    "niteagra",
    "mariayal",
    "alegarc2",
    "monhern2",
    "osmonroy",
    "kkarupas",
    "florodri",
]

for cec in cecs_who_joined:
    try:
        #get profile
        profile = Profile.objects.get(cec=cec)
        profile.distance += 5
        profile.save()
        check_badges(profile.user)
    except MultipleObjectsReturned:
        #check profile manually
        print(f"duplicated user {cec}, check manually")
    except Profile.DoesNotExist:
        pass