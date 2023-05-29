from django.db import models


class User(models.Model):
    username = models.CharField(max_length=256, unique=True, editable=False)
    access_token = models.CharField(max_length=256, unique=True, editable=False)
    user_uuid = models.CharField(max_length=256, unique=True, editable=False)
