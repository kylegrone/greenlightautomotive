# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0011_appointmentservice_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentrecommendation',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
