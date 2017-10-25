# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0014_dealer_carwash_flag_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentrecommendation',
            name='labor',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='appointmentrecommendation',
            name='parts',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='appointmentrecommendation',
            name='price_unit',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='appointmentrecommendation',
            name='service',
            field=models.ForeignKey(related_name='serrecommendation', default=None, blank=True, to='dealership.ServiceRepair', null=True),
        ),
    ]
