# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='walkaroundvehicleimage',
            name='dealer',
            field=models.ForeignKey(to='dealership.Dealer', null=True),
        )
    ]
