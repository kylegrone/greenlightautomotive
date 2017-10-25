# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livechat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('channel', models.CharField(max_length=b'2000')),
                ('guest_user', models.CharField(max_length=b'2000')),
                ('chat_dt', models.DateTimeField(auto_now_add=True)),
                ('advisor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
