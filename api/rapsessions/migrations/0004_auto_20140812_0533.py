# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.rapsessions.models


class Migration(migrations.Migration):

    dependencies = [
        ('rapsessions', '0003_auto_20140812_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapsession',
            name='clip',
            field=models.FileField(null=True, upload_to=api.rapsessions.models.get_clip_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='rapsession',
            name='thumbnail',
            field=models.FileField(null=True, upload_to=api.rapsessions.models.get_thumbnail_upload_path, blank=True),
        ),
    ]
