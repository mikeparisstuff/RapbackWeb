# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.rapsessions.models


class Migration(migrations.Migration):

    dependencies = [
        ('rapsessions', '0002_clip_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clip',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='clip',
            name='session',
        ),
        migrations.DeleteModel(
            name='Clip',
        ),
        migrations.AddField(
            model_name='rapsession',
            name='clip',
            field=models.FileField(default='', upload_to=api.rapsessions.models.get_clip_upload_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rapsession',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rapsession',
            name='thumbnail',
            field=models.FileField(default='', upload_to=api.rapsessions.models.get_thumbnail_upload_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rapsession',
            name='times_played',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rapsession',
            name='type',
            field=models.CharField(default=b'AUDIO', max_length=8, choices=[(b'AUDIO', b'Audio'), (b'VIDEO', b'Video')]),
            preserve_default=True,
        ),
    ]
