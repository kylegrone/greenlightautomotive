# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0017_auto_20161124_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='from_email',
            field=models.CharField(default=b'admin@greenlightautomotive.com', max_length=2000),
        ),
    ]
