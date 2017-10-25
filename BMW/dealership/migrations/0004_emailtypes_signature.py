# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0003_auto_20161025_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtypes',
            name='signature',
            field=models.TextField(null=True),
        ),
    ]
