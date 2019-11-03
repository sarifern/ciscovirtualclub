
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
    if url:
        user.profile.avatar = url
        user.save()