# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvisorCapacity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monday', models.BooleanField(default=True)),
                ('tuesday', models.BooleanField(default=True)),
                ('wednesday', models.BooleanField(default=True)),
                ('thursday', models.BooleanField(default=True)),
                ('friday', models.BooleanField(default=True)),
                ('saturday', models.BooleanField(default=True)),
                ('advisor', models.ForeignKey(related_name='advcapacity', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvisorRestrictions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monday', models.BooleanField(default=True)),
                ('tuesday', models.BooleanField(default=True)),
                ('wednesday', models.BooleanField(default=True)),
                ('thursday', models.BooleanField(default=True)),
                ('friday', models.BooleanField(default=True)),
                ('saturday', models.BooleanField(default=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('repeat', models.BooleanField(default=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('advisor', models.ForeignKey(related_name='advrestriction', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('confirmation_code', models.CharField(default=b'', max_length=2000, null=True, blank=True)),
                ('contact_me', models.BooleanField(default=False)),
                ('contact_time', models.CharField(default=b'', max_length=20)),
                ('driver_liscens_number', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('insurance_company_name', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('insurance_card_number', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('maintenance', models.BooleanField(default=False)),
                ('service_notes', models.TextField(default=None, max_length=2000, null=True, blank=True)),
                ('odometer_reading', models.CharField(max_length=255, null=True, blank=True)),
                ('comments', models.TextField(default=b'', max_length=2000, null=True)),
                ('checkin_time', models.DateTimeField(null=True, blank=True)),
                ('customer_signatures', models.TextField(default=None, null=True)),
                ('creditcard_id', models.CharField(max_length=2000, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('payment_id', models.CharField(max_length=2000, null=True)),
                ('reserve_wayaway', models.BooleanField(default=False)),
                ('appointment_reminder_status', models.BooleanField(default=False)),
                ('appointment_recommandation_status', models.BooleanField(default=False)),
                ('odometer_data', models.TextField(default=True, null=True, blank=True)),
                ('advisor', models.ForeignKey(related_name='advisorapt', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentRecommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Decline', max_length=10, choices=[(b'Accept', 'Accept'), (b'Decline', 'Decline')])),
                ('result', models.CharField(default=b'Fail', max_length=10, choices=[(b'Fail', 'Fail'), (b'Success', 'Success')])),
                ('date_advised', models.CharField(default=b'', max_length=200)),
                ('notes', models.CharField(default=b'', max_length=255)),
                ('appointment', models.ForeignKey(related_name='aptrecommendation', to='dealership.Appointment')),
                ('recommnded_by', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(null=True)),
                ('appointment', models.ForeignKey(related_name='appointmentservice', to='dealership.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Availability_Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='BMWResourceLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('rank', models.CharField(max_length=250, null=True)),
                ('url', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CapacityCounts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_tech', models.IntegerField(default=0)),
                ('time_slab', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(default=django.utils.timezone.now, null=True)),
                ('first_name', models.CharField(default=b'', max_length=255, null=True)),
                ('last_name', models.CharField(default=b'', max_length=255, null=True)),
                ('card_number', models.CharField(default=b'', max_length=255, null=True)),
                ('card_type', models.CharField(max_length=255, null=True, choices=[(b'Master', 'Master Card'), (b'Visa', 'Visa Card')])),
                ('card_exp_year', models.CharField(max_length=255, null=True, choices=[(b'2017', '2017'), (b'2018', '2018'), (b'2019', '2019'), (b'2020', '2020')])),
                ('card_exp_month', models.CharField(max_length=255, null=True, choices=[(b'01', '01'), (b'02', '02'), (b'03', '03'), (b'04', '04'), (b'05', '05'), (b'06', '06'), (b'07', '07'), (b'08', '08'), (b'09', '09'), (b'10', '10'), (b'11', '11'), (b'12', '12')])),
                ('card_ver_number', models.CharField(default=b'', max_length=255, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]{3}$', message=b'Enter 3 digits')])),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAdvisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('advisor', models.ForeignKey(related_name='mycustomers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerVehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=20, null=True, blank=True)),
                ('lisence_number', models.CharField(default=b'', max_length=20, null=True, blank=True)),
                ('milage', models.IntegerField(default=0, null=True, blank=True)),
                ('vin_number', models.CharField(default=None, max_length=50, null=True, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('vin_image', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('vin_process', models.BooleanField(default=False)),
                ('vin_data', models.TextField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('dealer_code', models.CharField(max_length=100, unique=True, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('timezone', models.CharField(max_length=10, null=True, blank=True)),
                ('consumer_access', models.BooleanField(default=True)),
                ('dms_access', models.BooleanField(default=False)),
                ('privacy_polilcy', models.FileField(null=True, upload_to=b'/Users/muhammadjavaidnasir/Documents/bmw/BMW/media', blank=True)),
                ('privacy_policy', models.TextField(null=True, blank=True)),
                ('message_of_the_day', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('webkey', models.CharField(max_length=250, null=True)),
                ('frameset_url', models.CharField(max_length=250, null=True)),
                ('service_url', models.CharField(max_length=250, null=True)),
                ('city', models.CharField(default=b'', max_length=2000, null=True, blank=True)),
                ('zipcode', models.CharField(default=b'', max_length=2000, null=True)),
                ('address_line1', models.TextField(default=b'', max_length=2000, null=True, blank=True)),
                ('address_line2', models.TextField(default=b'', max_length=2000, null=True, blank=True)),
                ('logo', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('ico_logo', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('client_id', models.TextField(default=b'', max_length=2000, null=True, blank=True)),
                ('secret', models.TextField(default=b'', max_length=2000, null=True, blank=True)),
                ('mode', models.CharField(max_length=250, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='shopcreatedby', to=settings.AUTH_USER_MODEL, null=True)),
                ('default_advisor', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DealerCapacity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeslot', models.DateTimeField()),
                ('available_technician', models.IntegerField()),
                ('dealer', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='DealerFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dealer', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='DealersVehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(related_name='dealervehiclecreatedby', to=settings.AUTH_USER_MODEL, null=True)),
                ('dealer', models.ForeignKey(related_name='dealervehicle', to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='DriverLiscenseIsurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('driver_liscens_number', models.CharField(max_length=255, null=True)),
                ('insurance_company_name', models.CharField(max_length=255, null=True)),
                ('insurance_card_number', models.CharField(max_length=255, null=True)),
                ('ins_exp_year', models.CharField(max_length=255, null=True, choices=[(b'2017', '2017'), (b'2018', '2018'), (b'2019', '2019'), (b'2020', '2020'), (b'2021', '2021'), (b'2022', '2022'), (b'2023', '2023'), (b'2024', '2024'), (b'2025', '2025')])),
                ('ins_exp_month', models.CharField(max_length=255, null=True, choices=[(b'01', '01'), (b'02', '02'), (b'03', '03'), (b'04', '04'), (b'05', '05'), (b'06', '06'), (b'07', '07'), (b'08', '08'), (b'09', '09'), (b'10', '10'), (b'11', '11'), (b'12', '12')])),
                ('date_added', models.DateField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('url_name', models.CharField(max_length=250, null=True)),
                ('url_qstring', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=255)),
                ('type', models.IntegerField(default=-1, choices=[(1, '1'), (2, '2'), (3, '3')])),
                ('customer_facing', models.BooleanField(default=False)),
                ('notes', models.CharField(default=b'', max_length=255, null=True)),
                ('color', models.CharField(default=b'', max_length=20)),
                ('dealer', models.ForeignKey(default=None, blank=True, to='dealership.Dealer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlagsHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.CharField(default=b'', max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True)),
                ('flag', models.ForeignKey(to='dealership.Flags')),
            ],
        ),
        migrations.CreateModel(
            name='InspectionCatagories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InspectionCategoriesItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='dealership.InspectionCatagories')),
            ],
        ),
        migrations.CreateModel(
            name='InspectionItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InspectionPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package', models.CharField(max_length=255)),
                ('dealer', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=10240)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('current_flag', models.CharField(default=b'flag1', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ReminderSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.BooleanField(default=False)),
                ('text', models.BooleanField(default=False)),
                ('phone', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReminderType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=20000)),
            ],
        ),
        migrations.CreateModel(
            name='ReportsHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_name', models.CharField(default=b'', max_length=255, null=True)),
                ('last_updated_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RO',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ro_number', models.CharField(unique=True, max_length=20)),
                ('rfid_tag', models.CharField(unique=True, max_length=20)),
                ('ro_date', models.DateTimeField(null=True)),
                ('flag1_updated_time', models.DateTimeField(default=None, null=True)),
                ('flag2_updated_time', models.DateTimeField(default=None, null=True)),
                ('flag3_updated_time', models.DateTimeField(default=None, null=True)),
                ('inspection_status', models.CharField(default=b'Required', max_length=20)),
                ('ro_status', models.BooleanField(default=True)),
                ('shop_notes', models.CharField(default=b'', max_length=255)),
                ('ro_completed', models.DateTimeField(null=True)),
                ('flag1', models.ForeignKey(related_name='flag1', default=None, blank=True, to='dealership.Flags', null=True)),
                ('flag1_updated_by', models.ForeignKey(related_name='flag1_user', default=None, to=settings.AUTH_USER_MODEL, null=True)),
                ('flag2', models.ForeignKey(related_name='flag2', default=None, blank=True, to='dealership.Flags', null=True)),
                ('flag2_updated_by', models.ForeignKey(related_name='flag2_user', default=None, to=settings.AUTH_USER_MODEL, null=True)),
                ('flag3', models.ForeignKey(related_name='flag3', default=None, blank=True, to='dealership.Flags', null=True)),
                ('flag3_updated_by', models.ForeignKey(related_name='flag3_user', default=None, to=settings.AUTH_USER_MODEL, null=True)),
                ('inspector', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observation', models.CharField(max_length=100, null=True)),
                ('recommendations', models.CharField(max_length=100, null=True)),
                ('specs', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(default=None, null=True, upload_to=b'')),
                ('status', models.CharField(default=b'pass', max_length=10)),
                ('inspection', models.ForeignKey(to='dealership.InspectionCategoriesItems')),
                ('inspector', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('ro', models.ForeignKey(to='dealership.RO')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRepair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('dms_opcode', models.CharField(max_length=20, null=True)),
                ('duration', models.CharField(max_length=10, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('price_unit', models.CharField(default=b'$', max_length=10)),
                ('flag_service', models.BooleanField(default=False)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to=b'')),
                ('type', models.CharField(max_length=1, choices=[(b's', b'Service'), (b'r', b'Repair')])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('labor', models.FloatField(default=0.0)),
                ('parts', models.FloatField(default=0.0)),
                ('availablity', models.ForeignKey(to='dealership.Availability_Status', null=True)),
                ('created_by', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True)),
                ('dealer', models.ForeignKey(related_name='ServiceRepair', default=None, to='dealership.Dealer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopAmenities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amenities', models.ForeignKey(to='dealership.Amenities')),
                ('shop', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='ShopHolidays',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True)),
                ('date', models.DateField(null=True)),
                ('updated_date', models.DateTimeField(default=None, null=True)),
                ('shop', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='ShopHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=250, null=True)),
                ('time_from', models.TimeField(null=True)),
                ('time_to', models.TimeField(null=True)),
                ('capacity_percent', models.IntegerField(default=60)),
                ('updated_date', models.DateTimeField(default=None, null=True)),
                ('shop', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='ShopOtherEmails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.TextField(null=True)),
                ('type', models.TextField(null=True)),
                ('updated_date', models.DateTimeField(default=None, null=True)),
                ('shop', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='ShopsContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.TextField(null=True)),
                ('email', models.TextField(null=True)),
                ('phone_work', models.TextField(null=True)),
                ('phone_cell', models.TextField(null=True)),
                ('updated_date', models.DateTimeField(default=None, null=True)),
                ('shop', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='ShopSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sms_no', models.TextField(null=True)),
                ('update_date', models.DateTimeField(default=None, null=True)),
                ('shop', models.ForeignKey(to='dealership.Dealer')),
            ],
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=96)),
                ('state_abbr', models.CharField(max_length=24, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(related_name='teamcreatedby', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamAdvisors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('advisor', models.ForeignKey(related_name='advisorteam', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(related_name='teamadvisorcreatedby', to=settings.AUTH_USER_MODEL, null=True)),
                ('team_id', models.ForeignKey(related_name='team', to='dealership.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TimeZones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('timezone', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDealer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dealer', models.ForeignKey(related_name='dealer', to='dealership.Dealer')),
                ('user', models.ForeignKey(related_name='userdealer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(default=None, max_length=255, null=True)),
                ('first_name', models.CharField(default=None, max_length=255, null=True)),
                ('last_name', models.CharField(default=None, max_length=255, null=True)),
                ('email_1', models.EmailField(default=None, max_length=255, null=True)),
                ('active_email', models.EmailField(max_length=255, null=True)),
                ('email_2', models.EmailField(default=None, max_length=255, null=True, blank=True)),
                ('active_email_date', models.DateField(default=None, null=True)),
                ('active_phone_number', models.CharField(default=None, max_length=2000, null=True, blank=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?(\\d|-){1,200}$', message=b'Invalid Phone Number')])),
                ('phone_number_1', models.CharField(default=None, max_length=2000, blank=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?(\\d|-){1,200}$', message=b'Invalid Phone Number')])),
                ('phone_number_2', models.CharField(default=None, max_length=2000, null=True, blank=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?(\\d|-){1,200}$', message=b'Invalid Phone Number')])),
                ('phone_number_3', models.CharField(default=None, max_length=2000, null=True, blank=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?(\\d|-){1,200}$', message=b'Invalid Phone Number')])),
                ('phone_1_type', models.CharField(default=b'Mobile', max_length=255, choices=[(b'Mobile', 'Mobile'), (b'Home', 'Home'), (b'Work', 'Work')])),
                ('phone_2_type', models.CharField(default=b'Home', max_length=255, choices=[(b'Mobile', 'Mobile'), (b'Home', 'Home'), (b'Work', 'Work')])),
                ('phone_3_type', models.CharField(default=b'Work', max_length=255, choices=[(b'Mobile', 'Mobile'), (b'Home', 'Home'), (b'Work', 'Work')])),
                ('active_phone_number_date', models.DateField(default=None, null=True)),
                ('terms_agreed', models.BinaryField(default=False)),
                ('token', models.CharField(default=None, max_length=255, null=True)),
                ('token_expiry', models.DateField(default=None, null=True, blank=True)),
                ('available_for_chat', models.BooleanField(default=False)),
                ('number_of_chats', models.IntegerField(default=0)),
                ('skip_confirmation', models.BooleanField(default=False)),
                ('mode_of_sending_updates', models.CharField(default=b'Email', max_length=20, choices=[(b'Email', 'Email'), (b'Text', 'Text'), (b'Call', 'Call')])),
                ('method_of_contact', models.CharField(default=b'Email', max_length=20, null=True, choices=[(b'Email', 'Email'), (b'Text', 'Text'), (b'Call', 'Call')])),
                ('avatar', models.ImageField(default=None, null=True, upload_to=b'')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(default=b'', max_length=2000, null=True)),
                ('zipcode', models.CharField(default=b'', max_length=2000, null=True)),
                ('address_line1', models.TextField(default=b'', max_length=2000, null=True)),
                ('address_line2', models.TextField(default=b'', max_length=2000, null=True, blank=True)),
                ('employee_no', models.CharField(default=None, max_length=255, null=True)),
                ('consumer_reserver', models.BooleanField(default=True)),
                ('customer_notes', models.TextField(default=b'', max_length=2000, null=True)),
                ('special_offer_notify', models.BooleanField(default=False)),
                ('carrier_choices', models.CharField(default=None, max_length=20, null=True, blank=True, choices=[(b'Verizon', 'Verizon'), (b'AT & T', 'AT & T')])),
                ('dealer', models.ForeignKey(default=None, to='dealership.Dealer', null=True)),
                ('question', models.ForeignKey(default=None, to='dealership.Questions', null=True)),
                ('state_us', models.ForeignKey(default=None, blank=True, to='dealership.States', null=True)),
                ('user', models.OneToOneField(related_name='userprofile', null=True, default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mainimage', models.ImageField(null=True, upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'')),
                ('default', models.BooleanField(default=False)),
                ('vehicle', models.ForeignKey(related_name='vehicleimage', to='dealership.Vehicle', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleParts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part_name', models.CharField(max_length=255, null=True)),
                ('vehicle', models.ForeignKey(to='dealership.Vehicle', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleTireWidth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=2, null=True, choices=[(b'RR', b'RR'), (b'RF', b'RF'), (b'LR', b'LR'), (b'LF', b'LF')])),
                ('width', models.CharField(max_length=255, null=True)),
                ('safe', models.BooleanField(default=True)),
                ('vehicle', models.ForeignKey(to='dealership.Vehicle', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VinMake',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('val', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VinModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('val', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VinTrim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('val', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VinYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('val', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WalkaroundInitials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('initials', models.TextField()),
                ('appointment', models.ForeignKey(to='dealership.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='walkaroundnotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('notes', models.TextField(null=True)),
                ('image', models.ImageField(default=None, null=True, upload_to=b'')),
                ('image_name', models.CharField(max_length=255, null=True)),
                ('other_category', models.CharField(max_length=255, null=True)),
                ('other_type', models.CharField(max_length=255, null=True)),
                ('LF', models.ForeignKey(related_name='LF', to='dealership.VehicleTireWidth', null=True)),
                ('LR', models.ForeignKey(related_name='LR', to='dealership.VehicleTireWidth', null=True)),
                ('RF', models.ForeignKey(related_name='RF', to='dealership.VehicleTireWidth', null=True)),
                ('RR', models.ForeignKey(related_name='RR', to='dealership.VehicleTireWidth', null=True)),
                ('appointment', models.ForeignKey(to='dealership.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='WalkaroundVehicleImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=None, null=True, upload_to=b'')),
                ('vehicle', models.ForeignKey(to='dealership.Vehicle', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WalkaroundVehicleMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=None, max_length=255, null=True)),
                ('coords', models.TextField(default=None, null=True)),
                ('name', models.CharField(default=None, max_length=255, null=True)),
                ('vehicleimage', models.ForeignKey(to='dealership.WalkaroundVehicleImage')),
            ],
        ),
        migrations.CreateModel(
            name='WayAway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(default=None, max_length=2000, null=True)),
                ('show_description', models.BooleanField(default=False)),
                ('show_dl', models.BooleanField(default=False)),
                ('popup_description', models.CharField(default=None, max_length=2000, null=True)),
                ('reserve_wayaway', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WayAwayDealer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=None, max_length=2000, null=True)),
                ('popup_description', models.CharField(default=None, max_length=2000, null=True)),
                ('dealer', models.ForeignKey(to='dealership.Dealer')),
                ('wayaway', models.ForeignKey(to='dealership.WayAway')),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='make',
            field=models.ForeignKey(related_name='makevehicles', to='dealership.VinMake'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='model',
            field=models.ForeignKey(related_name='modelvehicles', to='dealership.VinModel'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='year',
            field=models.ForeignKey(related_name='yearvehicles', to='dealership.VinYear'),
        ),
        migrations.AddField(
            model_name='remindersettings',
            name='customer',
            field=models.ForeignKey(to='dealership.UserProfile'),
        ),
        migrations.AddField(
            model_name='remindersettings',
            name='type',
            field=models.ForeignKey(to='dealership.ReminderType'),
        ),
        migrations.AddField(
            model_name='notes',
            name='created_by',
            field=models.ForeignKey(to='dealership.UserProfile'),
        ),
        migrations.AddField(
            model_name='notes',
            name='ro',
            field=models.ForeignKey(to='dealership.RO'),
        ),
        migrations.AddField(
            model_name='inspectioncategoriesitems',
            name='item',
            field=models.ForeignKey(to='dealership.InspectionItems'),
        ),
        migrations.AddField(
            model_name='inspectioncatagories',
            name='package',
            field=models.ForeignKey(to='dealership.InspectionPackage'),
        ),
        migrations.AddField(
            model_name='flagshistory',
            name='ro',
            field=models.ForeignKey(to='dealership.RO'),
        ),
        migrations.AddField(
            model_name='driverliscenseisurance',
            name='state',
            field=models.ForeignKey(default=None, to='dealership.States', null=True),
        ),
        migrations.AddField(
            model_name='driverliscenseisurance',
            name='user',
            field=models.OneToOneField(related_name='insuranceprofile', null=True, default=None, blank=True, to='dealership.UserProfile'),
        ),
        migrations.AddField(
            model_name='dealersvehicle',
            name='vehicle',
            field=models.ForeignKey(related_name='vehicledealer', to='dealership.Vehicle', null=True),
        ),
        migrations.AddField(
            model_name='dealerfavorites',
            name='favorites',
            field=models.ForeignKey(to='dealership.Favorites'),
        ),
        migrations.AddField(
            model_name='dealer',
            name='state_us',
            field=models.ForeignKey(default=None, blank=True, to='dealership.States', null=True),
        ),
        migrations.AddField(
            model_name='customervehicle',
            name='trim',
            field=models.ForeignKey(default=None, blank=True, to='dealership.VinTrim', null=True),
        ),
        migrations.AddField(
            model_name='customervehicle',
            name='user',
            field=models.ForeignKey(related_name='customervehicle', blank=True, to='dealership.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='customervehicle',
            name='vehicle',
            field=models.ForeignKey(related_name='vehicle', blank=True, to='dealership.Vehicle', null=True),
        ),
        migrations.AddField(
            model_name='customeradvisor',
            name='customer',
            field=models.ForeignKey(related_name='myadvisors', to='dealership.UserProfile'),
        ),
        migrations.AddField(
            model_name='customeradvisor',
            name='dealer',
            field=models.ForeignKey(to='dealership.Dealer'),
        ),
        migrations.AddField(
            model_name='creditcardinfo',
            name='user',
            field=models.OneToOneField(related_name='cc_profile', null=True, default=None, blank=True, to='dealership.UserProfile'),
        ),
        migrations.AddField(
            model_name='capacitycounts',
            name='dealer',
            field=models.ForeignKey(to='dealership.Dealer'),
        ),
        migrations.AddField(
            model_name='bmwresourcelink',
            name='shop',
            field=models.ForeignKey(to='dealership.Dealer'),
        ),
        migrations.AddField(
            model_name='appointmentservice',
            name='service',
            field=models.ForeignKey(related_name='service', to='dealership.ServiceRepair'),
        ),
        migrations.AddField(
            model_name='appointmentservice',
            name='technician',
            field=models.ForeignKey(related_name='apttechnician', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appointmentrecommendation',
            name='service',
            field=models.ForeignKey(related_name='serrecommendation', to='dealership.ServiceRepair'),
        ),
        migrations.AddField(
            model_name='appointmentrecommendation',
            name='technician',
            field=models.ForeignKey(related_name='aptrecomtechnician', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_status',
            field=models.ForeignKey(related_name='aptstatus', default=None, blank=True, to='dealership.AppointmentStatus', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='customer',
            field=models.ForeignKey(related_name='customerapt', blank=True, to='dealership.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='dealer',
            field=models.ForeignKey(default=None, blank=True, to='dealership.Dealer', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='ro',
            field=models.ForeignKey(related_name='ro', blank=True, to='dealership.RO', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='state_wayaway',
            field=models.ForeignKey(default=None, to='dealership.States', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='vehicle',
            field=models.ForeignKey(related_name='vehicleapt', blank=True, to='dealership.CustomerVehicle', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='way_away',
            field=models.ForeignKey(related_name='wayaway', blank=True, to='dealership.WayAway', null=True),
        ),
        migrations.AddField(
            model_name='advisorcapacity',
            name='shop',
            field=models.ForeignKey(related_name='shopcapacity', to='dealership.Dealer'),
        ),
    ]
