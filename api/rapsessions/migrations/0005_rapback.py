# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapsessions', '0004_auto_20140812_0533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rapback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('original', models.ForeignKey(to='rapsessions.RapSession')),
                ('response', models.ForeignKey(to='rapsessions.RapSession')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
