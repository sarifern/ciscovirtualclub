from django.contrib.staticfiles.storage import staticfiles_storage
from badgify.models import Award, Badge

Badge.objects.get_or_create(slug="42K", name="42K Milestone Achieved", description="You did it {username}! It's an Opportunity for more!",
                            image=staticfiles_storage.open('img/42k.png'))
Badge.objects.get_or_create(slug="30K", name="30K Milestone Achieved", description="Almost there {username}! Hold on your CONFIDENCE!",
                            image=staticfiles_storage.open('img/30k.png'))
Badge.objects.get_or_create(slug="21K", name="21K Milestone Achieved", description="Let's do this {username}! SOLIDARITY now or never!",
                            image=staticfiles_storage.open('img/21k.png'))
Badge.objects.get_or_create(slug="15K", name="15K Milestone Achieved", description="Excellent {username}! keep INSPIRING others!",
                            image=staticfiles_storage.open('img/15k.png'))
Badge.objects.get_or_create(slug="10K", name="10K Award Unlocked", description="Great {username}! COURAGE is your fuel!",
                            image=staticfiles_storage.open('img/10k.png'))
Badge.objects.get_or_create(slug="5K", name="5K Record Smashed", description="Good effort {username}!, Give me more!",
                            image=staticfiles_storage.open('img/5k.png'))
