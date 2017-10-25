# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
# import oauth2client.contrib.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0001_initial'),
    ]

#     operations = [
#         migrations.CreateModel(
#             name='CredentialsModel',
#             fields=[
#                 ('id', models.ForeignKey(primary_key=True, serialize=False, to='dealership.Appointment')),
#                 ('credential', oauth2client.contrib.django_orm.CredentialsField(null=True)),
#             ],
#         ),
#         migrations.CreateModel(
#             name='FlowModel',
#             fields=[
#                 ('id', models.ForeignKey(primary_key=True, serialize=False, to='dealership.Appointment')),
#                 ('flow', oauth2client.contrib.django_orm.FlowField(null=True)),
#             ],
#         ),
#     ]
