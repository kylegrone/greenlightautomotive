# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0006_remove_emailtypes_dealer'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='emailqueue',
            table=None,
        ),
    ]
