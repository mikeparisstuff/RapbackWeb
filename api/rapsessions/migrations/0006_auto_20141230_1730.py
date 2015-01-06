# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapsessions', '0005_rapback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapback',
            name='original',
            field=models.ForeignKey(related_name=b'original_set', to='rapsessions.RapSession'),
        ),
        migrations.AlterField(
            model_name='rapback',
            name='response',
            field=models.ForeignKey(related_name=b'response_set', to='rapsessions.RapSession'),
        ),
    ]
