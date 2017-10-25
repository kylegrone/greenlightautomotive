# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0004_emailtypes_signature'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailQueue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created_time', models.DateTimeField(null=True)),
                ('subject', models.CharField(max_length=255)),
                ('cc', models.TextField(null=True)),
                ('bcc', models.TextField(null=True)),
                ('params', models.TextField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('mail_time', models.DateTimeField(null=True)),
                ('sent_time', models.DateTimeField(null=True)),
                ('mail_error', models.IntegerField(default=0)),
                ('mail_retries', models.IntegerField(default=0)),
                ('mail_failuire_date', models.DateTimeField(null=True)),
                ('mail_detail', models.TextField(null=True)),
                ('mail_from', models.TextField(default=b'')),
                ('mail_to', models.TextField(default=b'')),
                ('mail_error_detail', models.TextField(null=True)),
                ('attachments', models.TextField(null=True)),
                ('type', models.ForeignKey(to='dealership.EmailTypes')),
            ],
            options={
                'db_table': 'api_application_email_queue',
            },
        ),
    ]
