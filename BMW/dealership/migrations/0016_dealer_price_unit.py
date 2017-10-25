# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0015_auto_20161124_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='price_unit',
            field=models.CharField(default=b'$', max_length=10),
        ),
    ]
