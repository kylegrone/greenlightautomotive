# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dealership', '0009_auto_20161025_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentservice',
            name='price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customervehicle',
            name='customer_vehicle_desc',
            field=models.TextField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='advisor',
            field=models.ForeignKey(related_name='advisorapt', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='appointmentrecommendation',
            name='recommnded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='appointmentrecommendation',
            name='technician',
            field=models.ForeignKey(related_name='aptrecomtechnician', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='appointmentservice',
            name='technician',
            field=models.ForeignKey(related_name='apttechnician', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='created_by',
            field=models.ForeignKey(related_name='shopcreatedby', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='default_advisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='privacy_polilcy',
            field=models.FileField(null=True, upload_to=b'/Users/muhammadjavaidnasir/Documents/bmw/BMW/media', blank=True),
        ),
        migrations.AlterField(
            model_name='dealersvehicle',
            name='created_by',
            field=models.ForeignKey(related_name='dealervehiclecreatedby', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='flagshistory',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='ro',
            name='flag1_updated_by',
            field=models.ForeignKey(related_name='flag1_user', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='ro',
            name='flag2_updated_by',
            field=models.ForeignKey(related_name='flag2_user', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='ro',
            name='flag3_updated_by',
            field=models.ForeignKey(related_name='flag3_user', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='ro',
            name='inspector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='roinspection',
            name='inspector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='servicerepair',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='created_by',
            field=models.ForeignKey(related_name='teamcreatedby', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='teamadvisors',
            name='created_by',
            field=models.ForeignKey(related_name='teamadvisorcreatedby', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
