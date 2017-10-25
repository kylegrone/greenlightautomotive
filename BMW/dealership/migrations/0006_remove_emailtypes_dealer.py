# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0005_emailqueue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailtypes',
            name='dealer',
        ),
    ]
