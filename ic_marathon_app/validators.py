from django.core.exceptions import ValidationError



def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError(
            "The maximum file size that can be uploaded is 5MB")
    else:
        return value


def validate_workout_time(value):
    total_min = value.hour*60+value.minute
    if total_min < 14:
        raise ValidationError("The minimum time value for a workout is 15 min")
    else:
        return value

def validate_distance(value):
    if float(value.real) > 99.99:
        raise ValidationError("The maximum distance value for a workout is 99.99 km")
    else:
        return value
    