# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0023_auto_20170301_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='pickup_flag_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dealer',
            name='queue_flag_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dealer',
            name='servicecomplete_flag_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dealer',
            name='workingonvehicle_flag_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
