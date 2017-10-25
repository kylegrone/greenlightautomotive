# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0024_auto_20170301_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walkaroundnotes',
            name='image_name',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
    ]
