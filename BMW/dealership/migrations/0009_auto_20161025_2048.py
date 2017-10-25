# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0008_emailtypes_dealer'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMultimedia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('multimedia_file', models.CharField(max_length=255)),
                ('dealer', models.ForeignKey(default=None, blank=True, to='dealership.Dealer', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='emailqueue',
            name='attachments',
        ),
        migrations.AddField(
            model_name='emailqueue',
            name='dealer',
            field=models.ForeignKey(default=None, blank=True, to='dealership.Dealer', null=True),
        ),
    ]
