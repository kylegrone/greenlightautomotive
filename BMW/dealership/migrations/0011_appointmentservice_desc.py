# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0010_auto_20161122_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentservice',
            name='desc',
            field=models.TextField(default=None, null=True, blank=True),
        ),
    ]
