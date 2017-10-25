# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0002_auto_20161016_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTypes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('template', models.TextField()),
                ('html_template', models.TextField(null=True)),
                ('subject', models.TextField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='dealer',
            name='privacy_polilcy',
            field=models.FileField(null=True, upload_to=b'D:\\velocity\\BMW_NEW\\BMW\\media', blank=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='timezone',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='emailtypes',
            name='dealer',
            field=models.ForeignKey(default=None, blank=True, to='dealership.Dealer', null=True),
        ),
    ]
