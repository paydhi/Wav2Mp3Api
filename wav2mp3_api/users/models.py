import uuid

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=256, unique=True, null=False, blank=False)
    access_token = models.UUIDField(max_length=64, default=uuid.uuid4, editable=False)
    user_uuid = models.UUIDField(max_length=64, default=uuid.uuid4, editable=False)
