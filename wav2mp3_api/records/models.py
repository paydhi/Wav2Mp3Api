import uuid

from django.db import models
from users.models import User


class Record(models.Model):
    record_uuid = models.UUIDField(max_length=64, default=uuid.uuid4, editable=False)
    record = models.FileField(upload_to='uploads/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

