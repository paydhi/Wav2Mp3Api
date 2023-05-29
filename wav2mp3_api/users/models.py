import uuid

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    user_token = models.CharField(max_length=100)
    user_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)