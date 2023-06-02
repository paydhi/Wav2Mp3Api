import os
import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.models import User


class Record(models.Model):
    record_uuid = models.UUIDField(max_length=64, default=uuid.uuid4, editable=False, unique=True)
    record = models.FileField(upload_to='uploads/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(pre_delete, sender=Record)
def delete_related_file(sender, instance, **kwargs):
    if instance.record:
        if os.path.isfile(instance.record.path):
            os.remove(instance.record.path)
