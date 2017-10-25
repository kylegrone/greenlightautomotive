# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0012_appointmentrecommendation_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='approval_needed_flag_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
