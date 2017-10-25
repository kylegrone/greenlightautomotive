# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0019_auto_20161128_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customervehicle',
            name='vin_image',
            field=models.ImageField(null=True, upload_to=b''),
        ),
    ]
