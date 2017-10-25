# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0007_auto_20161025_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtypes',
            name='dealer',
            field=models.ForeignKey(default=None, blank=True, to='dealership.Dealer', null=True),
        ),
    ]
