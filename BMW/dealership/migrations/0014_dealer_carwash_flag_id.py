# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0013_dealer_approval_needed_flag_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='carwash_flag_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
