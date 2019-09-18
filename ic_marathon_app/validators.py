from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size
    
    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value


def validate_workout_time(value):
        
    if value < 15:
        raise ValidationError("The minimum time value for a workout is 15 min")
    else:
        return value
