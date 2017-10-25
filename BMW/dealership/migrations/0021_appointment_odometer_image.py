# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0020_auto_20161129_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='odometer_image',
            field=models.ImageField(default=None, null=True, upload_to=b'', blank=True),
        ),
    ]
