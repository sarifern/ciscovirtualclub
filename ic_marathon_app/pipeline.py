from .models import Profile

def get_avatar(backend, strategy, details, response,
         *args, **kwargs):
    url = None
    user=kwargs.get('user')
    if backend.name == 'facebook':
        url = response.get('picture').get('data').get('url')
    if backend.name == 'instagram':
        url = response.get('user').get('profile_picture')
    if backend.name == 'google-oauth2':
        url = response.get('picture')
    if backend.name == 'linkedin-oauth2':
        url = 'https://ciscorunning2020.s3.amazonaws.com/static/img/generic_avatar.jpg'
    if url:
        profile = Profile.objects.get_or_create(user=user)[0]
        profile.avatar = url
        profile.save()
        user.profile = profile
        user.save()