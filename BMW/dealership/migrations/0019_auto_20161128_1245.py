# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0018_dealer_from_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentrecommendation',
            name='notes',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
