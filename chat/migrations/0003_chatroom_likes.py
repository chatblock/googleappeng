# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20160419_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
