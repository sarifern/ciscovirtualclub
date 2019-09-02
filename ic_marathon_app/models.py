from django.db import models
import uuid
from .validators import validate_file_size
# Create your models here.


class Workout(models.Model):
    belongs_to = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, default=None)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2)
    photo_evidence = models.ImageField(validators=[validate_file_size])
