# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0022_dealer_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='prestagevehicle_flag_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        )
    ]
