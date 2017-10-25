# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0021_appointment_odometer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='number',
            field=models.CharField(default=b'', max_length=2000),
        ),
    ]
