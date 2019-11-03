from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size
    
    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value


def validate_workout_time(value):
        
    if value < 14:
        raise ValidationError("The minimum time value for a workout is 15 min")
    else:
        return value

def validate_team_members(value):
    from ic_marathon_app.models import Profile
    temp_team = value
    associated_members = Profile.objects.filter(team__team_name=temp_team.team_name)

    if associated_members > 3:
        raise ValidationError("The maximum number of members for this team has already been reached. Please join (or create) a different team")
    else:
        return value