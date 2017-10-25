# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0016_dealer_price_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentrecommendation',
            name='price_unit',
            field=models.CharField(default=b'$', max_length=10),
        ),
    ]
