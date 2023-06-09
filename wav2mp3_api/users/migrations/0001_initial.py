# Generated by Django 4.2.1 on 2023-05-29 18:06

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256, unique=True)),
                ('access_token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('user_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
