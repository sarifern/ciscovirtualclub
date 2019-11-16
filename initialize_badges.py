from django.contrib.staticfiles.storage import staticfiles_storage
from badgify.models import Award, Badge

Badge.objects.get_or_create(slug="168K", name="168K", description="People who have run 168K",
                            image=staticfiles_storage.open('img/168k.png'))
Badge.objects.get_or_create(slug="126K", name="126K", description="People who have run 126K",
                            image=staticfiles_storage.open('img/126k.png'))
Badge.objects.get_or_create(slug="84K", name="84K", description="People who have run 84K",
                            image=staticfiles_storage.open('img/84k.png'))
Badge.objects.get_or_create(slug="42K", name="42K", description="People who have run 42K",
                            image=staticfiles_storage.open('img/42k.png'))
Badge.objects.get_or_create(slug="21K", name="21K", description="People who have run 21K",
                            image=staticfiles_storage.open('img/21k.png'))
Badge.objects.get_or_create(slug="10K", name="10K", description="People who have run 10K",
                            image=staticfiles_storage.open('img/10k.png'))
