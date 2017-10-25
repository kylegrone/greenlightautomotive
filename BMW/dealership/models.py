from datetime import date
import datetime

from django import utils
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import signals
from django.template.defaultfilters import default
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from dealership.services.pusherservice import PusherService


class VinMake(models.Model):
    name = models.CharField(max_length=200)
    val = models.CharField(max_length=200)
    
    
    
class VinModel(models.Model):
    name = models.CharField(max_length=200)
    val = models.CharField(max_length=200)
    
    
    
      
class VinYear(models.Model):
    name = models.CharField(max_length=200)
    val = models.CharField(max_length=200)   
    
    
    
    
class VinTrim(models.Model):
    name = models.CharField(max_length=200)
    val = models.CharField(max_length=200)    

# Create your models here.
class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    

class States(models.Model):  
    id = models.IntegerField(primary_key=True)  
    name = models.CharField(max_length=96)  
    state_abbr = models.CharField(max_length=24, blank=True)
    
 

    

class Dealer(models.Model):
    name = models.CharField(max_length=100, null = True)
    dealer_code = models.CharField(max_length=100, null = True,unique=True)       
    description = models.TextField(null = True,blank=True)
    timezone = models.CharField(max_length=255, null = True,blank=True)
    consumer_access = models.BooleanField(default=True,blank=True)
    dms_access = models.BooleanField(default=False,blank=True)
    privacy_polilcy = models.FileField(null=True,upload_to=settings.MEDIA_ROOT,blank=True) 
    privacy_policy = models.TextField(null = True,blank=True)
    message_of_the_day = models.TextField(null = True,blank=True)
    created_by = models.ForeignKey(User, null=True, related_name="shopcreatedby",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default = utils.timezone.now )
    webkey = models.CharField(max_length=250, null = True)
    frameset_url = models.CharField(max_length=250, null= True)
    service_url = models.CharField(max_length=250, null= True)
    #country = CountryField()
    state_us = models.ForeignKey(States,null=True,default=None,blank=True)
    city = models.CharField(max_length=2000,default='',null=True,blank=True)
    zipcode = models.CharField(max_length=2000,default='',null=True)
    address_line1 = models.TextField(max_length=2000,default='',null=True,blank=True)
    address_line2 =  models.TextField(max_length=2000,default='',null=True,blank=True)
    default_advisor = models.ForeignKey(User,blank=True,default=None,null=True,on_delete=models.SET_NULL)
    logo = models.ImageField(null=True,default=None,blank=True)
    ico_logo = models.ImageField(null=True,default=None,blank=True)
    client_id =  models.TextField(max_length=2000,default='',null=True,blank=True)
    secret =  models.TextField(max_length=2000,default='',null=True,blank=True)
    mode = models.CharField(max_length=250, null= True,blank=True)
    approval_needed_flag_id = models.IntegerField(default=None,blank=True,null=True)
    carwash_flag_id = models.IntegerField(default=None,blank=True,null=True)
    price_unit = models.CharField(max_length=10,default='$',null=False)
    from_email = models.CharField(max_length=2000,default='admin@greenlightautomotive.com',null=False)
    number = models.CharField(max_length=2000,default='',null=False)
    prestagevehicle_flag_id = models.IntegerField(default=None,blank=True,null=True)
    queue_flag_id = models.IntegerField(default=None,blank=True,null=True)
    pickup_flag_id = models.IntegerField(default=None,blank=True,null=True)
    workingonvehicle_flag_id = models.IntegerField(default=None,blank=True,null=True)
    servicecomplete_flag_id = models.IntegerField(default=None,blank=True,null=True)
    
class CapacityCounts(models.Model):
    total_tech = models.IntegerField(default=0)
    time_slab = models.DateTimeField(null=True , default=None)
    dealer = models.ForeignKey(Dealer)   
    
    
class UserProfile(models.Model):
    
    """this is the validaion rulese checked in database """
    def clean(self):
        from dealership.services.userservices import UserService
        userservice = UserService()
        error = False
        errors = {}
        if self.phone_number_1 and self.phone_number_1 != 0:
            self.phone_number_1 = self.phone_number_1.replace("-","")
            if userservice.check_phone_exist(self, self.phone_number_1):
                error = True
                errors["phone_number_1"] = _('Phone Number already exists.')

            
        if self.phone_number_2 and self.phone_number_2 != "0":
                self.phone_number_2 = self.phone_number_2.replace("-","")
                if userservice.check_phone_exist(self, self.phone_number_2):
                    error = True
                    errors["phone_number_2"] = _('Phone Number already exists.')
            
        if self.phone_number_3 and self.phone_number_3 != "0":
                self.phone_number_3 = self.phone_number_3.replace("-","")
                if userservice.check_phone_exist(self, self.phone_number_3):
                    error = True
                    errors["phone_number_3"] = _('Phone Number already exists.')
              
        if self.active_phone_number and  self.active_phone_number != "0":
               
                if userservice.check_phone_exist(self, self.active_phone_number):
                    error = True
                    errors["active_phone_number"] = _('Phone Number already exists.')
                    
        if self.email_1  and self.email_1 != "":
                if userservice.check_email_exist(self,self.email_1):
                    error = True
                    errors["email_1"] = _('Email already exists.')
        if self.email_2 and self.email_2 != "":
                if userservice.check_email_exist(self,self.email_2):
                    error = True
                    errors["email_2"] = _('Email already exists.')   
        if self.active_email and self.active_email != ""  :
                print self.active_email
                if userservice.check_email_exist(self,self.active_email):
                    error = True
                    errors["active_email"] = _('Email already exists.') 

                    
                     
        if error :
            raise ValidationError(errors)
      
        
    PHONE_CHOICES = (
    ("Mobile", _("Mobile")),
    ("Home", _("Home")),
    ("Work", _("Work")),
    
    )
    PREFFERED_CHOICES = (
                         ("Email", _("Email")),
                         ("Text", _("Text")),
                         ("Call", _("Call")),
    )
    CARRIER_CHOICES = (
                         ("Verizon", _("Verizon")),
                         ("AT & T", _("AT & T")),
                         
    )
    phone_regex = RegexValidator(regex=r'^\+?1?(\d|-){1,200}$', message="Invalid Phone Number")
    question =  models.ForeignKey(Questions,null=True,default=None)
    answer = models.CharField(max_length=255,null=True,default=None)
    first_name = models.CharField(max_length=255, null = True,default=None)
    last_name = models.CharField(max_length=255, null = True,default=None)
    email_1 = models.EmailField(max_length=255,null =True,default=None)
    active_email = models.EmailField(max_length=255,null =True)
    email_2 = models.EmailField(max_length=255,null =True,default=None,blank=True)
    active_email_date = models.DateField(null=True,default=None) 
    active_phone_number =  models.CharField(null=True, validators=[phone_regex], blank=True,max_length=2000,default=None)
    phone_number_1 =  models.CharField(validators=[phone_regex], blank=True,max_length=2000,default=None)
    phone_number_2=models.CharField(validators=[phone_regex],null=True, blank=True,max_length=2000,default=None)
    phone_number_3=models.CharField(validators=[phone_regex],null=True, blank=True,max_length=2000,default=None)
    phone_1_type = models.CharField(max_length=255,choices=PHONE_CHOICES, default='Mobile')
    phone_2_type = models.CharField(max_length=255, choices=PHONE_CHOICES, default='Home')
    phone_3_type = models.CharField(max_length=255, choices=PHONE_CHOICES, default='Work')
    active_phone_number_date = models.DateField(null=True,default=None)
    terms_agreed = models.BinaryField(default=False)
    token = models.CharField(max_length=255, null = True,default=None)
    token_expiry = models.DateField(default=None, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="userprofile",null=True,default=None)
    available_for_chat = models.BooleanField(default=False)
    number_of_chats = models.IntegerField(default=0)
    skip_confirmation = models.BooleanField(default=False)
    mode_of_sending_updates = models.CharField(max_length=20,choices = PREFFERED_CHOICES ,default='Email',null=False)
    method_of_contact = models.CharField(max_length=20,choices = PREFFERED_CHOICES ,default='Email',null=True)
    avatar = models.ImageField(null=True,default=None)
    country = CountryField()
    state_us = models.ForeignKey(States,null=True,default=None,blank=True)
    city = models.CharField(max_length=2000,default='',null=True)
    zipcode = models.CharField(max_length=2000,default='',null=True)
    address_line1 = models.TextField(max_length=2000,default='',null=True)
    address_line2 =  models.TextField(max_length=2000,default='',null=True,blank=True)
    dealer = models.ForeignKey(Dealer, null=True,default=None)
    employee_no = models.CharField(max_length=255,null=True , default=None)
    consumer_reserver = models.BooleanField(default=True)
    customer_notes = models.TextField(max_length=2000,default='',null=True)
    special_offer_notify = models.BooleanField(default=False)
    carrier_choices = models.CharField(max_length=20,choices = CARRIER_CHOICES ,default=None,blank=True, null=True)
#     customer_advisor =  models.ForeignKey(User, null=True,default=None,related_name="advcustomers")
    
    
class CreditCardInfo(models.Model):
    last_3_regex = RegexValidator(regex=r'^[0-9]{3}$', message="Enter 3 digits")
    CARD_CHOICES = (
                    ("Master", _("Master Card")),
                    ("Visa", _("Visa Card")),
    )
    YEARS_CHOICE =(
             ("2017", _("2017")),
                    ("2018", _("2018")), ("2019", _("2019")), ("2020", _("2020")),
            )
    
#     ("2017"),_("2017"),("2018"),_("2018"),("2019"),_("2019"),("2020"),_("2020"),("2021"),_("2021"),("2022"),_("2022"),
#             ("2023"),_("2023"),("2024"),_("2024"),
#             ("2025"),_("2025"),("2026"),_("2026"),("2027"),_("2027"),("2028"),_("2028"),("2029"),_("2029"),("2030"),_("2030")
    MONTH_CHOICE = (
                    ("01", _("01")),("02", _("02")),("03", _("03")),("04", _("04")),("05", _("05")),("06", _("06")),
                    ("07", _("07")),("08", _("08")),("09", _("09")),("10", _("10")),("11", _("11")),("12", _("12"))
    )
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE,related_name="cc_profile",null=True,blank=True,default=None) 
    date_added =  models.DateField(null=True,default= utils.timezone.now) 
    first_name = models.CharField(null=True,default="",max_length=255)
    last_name = models.CharField(null=True,default="",max_length=255)     
    card_number = models.CharField(null=True,default="",max_length=255)
    card_type = models.CharField(null=True,choices=CARD_CHOICES,max_length=255)
    card_exp_year = models.CharField(null=True,choices=YEARS_CHOICE,max_length=255)
    card_exp_month = models.CharField(null=True,choices=MONTH_CHOICE,max_length=255)
    card_ver_number = models.CharField(null=True,default="",max_length=255,validators = [last_3_regex])
    

class DriverLiscenseIsurance(models.Model):
    YEARS_CHOICE =(
             ("2017", _("2017")),
             ("2018", _("2018")),
             ("2019", _("2019")),
             ("2020", _("2020")),
             ("2021", _("2021")),
             ("2022", _("2022")),
             ("2023", _("2023")),
             ("2024", _("2024")),
             ("2025", _("2025")),
            )
    MONTH_CHOICE = (
                    ("01", _("01")),("02", _("02")),("03", _("03")),("04", _("04")),("05", _("05")),("06", _("06")),
                    ("07", _("07")),("08", _("08")),("09", _("09")),("10", _("10")),("11", _("11")),("12", _("12"))
    )
    state = models.ForeignKey(States,null=True,default=None)
    driver_liscens_number = models.CharField(max_length=255,null=True)
    insurance_company_name = models.CharField(max_length=255,null=True)
    insurance_card_number = models.CharField(max_length=255,null=True)
    ins_exp_year = models.CharField(null=True,choices=YEARS_CHOICE,max_length=255)
    ins_exp_month = models.CharField(null=True,choices=MONTH_CHOICE,max_length=255)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE,related_name="insuranceprofile",null=True,blank=True,default=None)
    date_added =  models.DateField(null=True,default= utils.timezone.now) 
          
    
class CustomerAdvisor(models.Model):   
    customer = models.ForeignKey(UserProfile, related_name="myadvisors")
    advisor = models.ForeignKey(User, related_name="mycustomers")
    dealer =models.ForeignKey(Dealer)
    
    
    
class Vehicle(models.Model):
    make = models.ForeignKey(VinMake,related_name="makevehicles") #max_length=255, null = False)
    model = models.ForeignKey(VinModel,related_name="modelvehicles") #models.CharField(max_length=255, null = False)

    year = models.ForeignKey(VinYear,related_name="yearvehicles")#models.CharField(max_length=255, null = False)
    mainimage = models.ImageField(null=True) 
    
    
class VehicleParts(models.Model):
    vehicle = models.ForeignKey(Vehicle , null=True)
    part_name = models.CharField(max_length=255, null=True)
    
class VehicleTireWidth(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    TYPELIST = (('RR', 'RR'), ('RF', 'RF'),('LR', 'LR'), ('LF', 'LF')) 
    type = models.CharField(max_length=2, choices=TYPELIST,null=True)
    width = models.CharField(max_length = 255 , null=True)
    safe = models.BooleanField(default=True)
    
class VehicleImages(models.Model):
    vehicle = models.ForeignKey(Vehicle,null=True, related_name="vehicleimage")
    image = models.ImageField(null=True) 
    default = models.BooleanField(default=False)
    
    
    
class CustomerVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle,null=True, related_name="vehicle",blank=True)
    user = models.ForeignKey(UserProfile, null=True, related_name="customervehicle",blank=True)
    color = models.CharField(max_length=20, null = True,blank=True)
    lisence_number = models.CharField(max_length=20, null = True,blank=True,default="")
    milage = models.IntegerField(default=0,blank=True,null=True)
    vin_number = models.CharField(max_length=50, null = True,default=None,blank=True)
    created_at = models.DateTimeField(default = utils.timezone.now)
    vin_image = models.ImageField(null=True,default=None,blank=True) 
    vin_process = models.BooleanField(default=False)
    trim = models.ForeignKey(VinTrim,default=None,blank=True,null=True)
    vin_data = models.TextField(default=None,blank=True,null=True)
    vin_image = models.ImageField(null=True) 
    customer_vehicle_desc = models.TextField(default=None,blank=True,null=True)
    
class Team(models.Model):
    name = models.CharField(max_length=100, null = True)
    created_by = models.ForeignKey(User, null=True, related_name="teamcreatedby",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default = utils.timezone.now)
    
class TeamAdvisors(models.Model):
    team_id = models.ForeignKey(Team, null=False, related_name="team")
    advisor = models.ForeignKey(User, null=False, related_name="advisorteam")
    created_by = models.ForeignKey(User, null=True, related_name="teamadvisorcreatedby",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default = utils.timezone.now)
    
class DealersVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle,null=True, related_name="vehicledealer")
    dealer = models.ForeignKey(Dealer, null=False, related_name="dealervehicle")
    created_by = models.ForeignKey(User, null=True, related_name="dealervehiclecreatedby",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default = utils.timezone.now)
    
    

class UserDealer(models.Model):
    dealer = models.ForeignKey(Dealer, null=False, related_name="dealer")
    user = models.ForeignKey(User, null=False, related_name="userdealer")
    
# class Shops(models.Model):


class ShopsContact(models.Model):
    id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Dealer)
    name = models.TextField(null = True)
    email = models.TextField(null = True)
    phone_work = models.TextField(null = True)
    phone_cell = models.TextField(null = True)
    updated_date = models.DateTimeField(null=True,default=None)
    
class ShopOtherEmails(models.Model):
    shop = models.ForeignKey(Dealer)
    email = models.TextField(null=True)
    type = models.TextField(null=True)
    updated_date = models.DateTimeField(null=True , default=None)
    
class ShopSMS(models.Model):
    shop = models.ForeignKey(Dealer)
    sms_no = models.TextField(null=True)
    update_date = models.DateTimeField(null=True , default = None)
    
class ShopHours(models.Model):
    shop =  models.ForeignKey(Dealer)
    day = models.CharField(max_length = 250, null = True) 
    time_from = models.TimeField(null = True)  
    time_to = models.TimeField(null = True)
    capacity_percent = models.IntegerField(default=60)
    updated_date = models.DateTimeField(null=True , default=None)
    
class ShopHolidays(models.Model):
    shop = models.ForeignKey(Dealer)
    description = models.TextField(null=True)
    date = models.DateField(null = True)
    updated_date = models.DateTimeField(null=True , default=None)
    
class Amenities(models.Model):
    name = models.CharField(max_length = 250 , null= True)
    
class Favorites(models.Model):
    name =   models.CharField(max_length=250, null=False)
    url_name = models.CharField(max_length = 250 , null= True)
    url_qstring = models.CharField(max_length = 500 , null= True)
    
class DealerFavorites(models.Model):
    dealer = models.ForeignKey(Dealer)
    favorites = models.ForeignKey(Favorites)
    
class DealerCapacity(models.Model):
    dealer = models.ForeignKey(Dealer)
    timeslot = models.DateTimeField()
    available_technician = models.IntegerField()    
    
class ShopAmenities(models.Model):
    shop = models.ForeignKey(Dealer)
    amenities = models.ForeignKey(Amenities)
    
class BMWResourceLink(models.Model):
    shop = models.ForeignKey(Dealer)
    name = models.CharField(max_length = 250 , null = True)
    rank =  models.CharField(max_length = 250 , null=True)
    url = models.CharField(max_length = 250 , null = True)

class TimeZones(models.Model):
    name = models.CharField(max_length = 250 , null = True)
    timezone = models.CharField(max_length = 250 , null = True)
          
class WayAway(models.Model):
    name = models.CharField(max_length=100, null = True)
    description = models.CharField(max_length=2000,null=True,default=None)
    show_description = models.BooleanField(default=False)
    show_dl = models.BooleanField(default=False)
    popup_description = models.CharField(max_length=2000,null=True,default=None )
    reserve_wayaway = models.BooleanField(default=False)
    
    
class WayAwayDealer(models.Model):
    dealer = models.ForeignKey(Dealer)
    wayaway = models.ForeignKey(WayAway)
    description = models.CharField(max_length=2000,null=True,default=None )
    popup_description = models.CharField(max_length=2000,null=True,default=None )
    
    
class Availability_Status(models.Model):
    name = models.CharField(max_length = 250)
        
class ServiceRepair(models.Model):
    name = models.CharField(max_length=250, null = True) 
    dms_opcode = models.CharField(max_length=20, null = True)
    duration = models.CharField(max_length=10, null = True)
    price = models.FloatField(default=0.0)
    price_unit = models.CharField(max_length=10, default = '$')
    flag_service = models.BooleanField(default=False)
    description = models.TextField(null = True)
    image = models.ImageField(null=True) 
    TYPELIST = (('s', 'Service'), ('r', 'Repair')) 
    type = models.CharField(max_length=1, choices=TYPELIST)
    created_at = models.DateTimeField(default = utils.timezone.now)
    created_by = models.ForeignKey(User,default=None,null=True,on_delete=models.SET_NULL)
    dealer = models.ForeignKey(Dealer,related_name="ServiceRepair",default=None,null=True)
    labor = models.FloatField(default=0.0)
    parts = models.FloatField(default=0.0)
    availablity = models.ForeignKey(Availability_Status,null=True)
    
        
class AppointmentStatus(models.Model):
    name = models.CharField(max_length=100, null = True)
    
    
    
class Flags(models.Model):
    FLAGS_CHOICE = (
                    (1, _("1")),(2, _("2")),(3, _("3"))
    )
   
    name = models.CharField(max_length=255,null=False,default=None)
    type =  models.IntegerField(choices=FLAGS_CHOICE,null=False,default=-1)
    customer_facing = models.BooleanField(null=False,default=False)
    notes = models.CharField(max_length=255,null=True,default="")
    color = models.CharField(max_length=20,null=False,default="")
    dealer = models.ForeignKey(Dealer,blank=True,default=None,null=True)
    
class RO(models.Model):
   
    ro_number = models.CharField(max_length=20,null=False,unique=True)
    rfid_tag = models.CharField(max_length=20,null=False,unique=True)
    ro_date = models.DateTimeField(null=True)
    flag1 = models.ForeignKey(Flags,null=True,default=None,blank=True,related_name="flag1")
    flag2 = models.ForeignKey(Flags,null=True,default=None,blank=True,related_name="flag2")
    flag3 = models.ForeignKey(Flags,null=True,default=None,blank=True,related_name="flag3")
    flag1_updated_time = models.DateTimeField(null=True,default=None)
    flag2_updated_time = models.DateTimeField(null=True,default=None)
    flag3_updated_time = models.DateTimeField(null=True,default=None)
    flag1_updated_by = models.ForeignKey(User,null=True,default=None,related_name="flag1_user",on_delete=models.SET_NULL)
    flag2_updated_by = models.ForeignKey(User,null=True,default=None,related_name="flag2_user",on_delete=models.SET_NULL)
    flag3_updated_by = models.ForeignKey(User,null=True,default=None,related_name="flag3_user",on_delete=models.SET_NULL)
    inspection_status = models.CharField(max_length=20,default="Required")
    ro_status = models.BooleanField(default=True)
    inspector = models.ForeignKey(User,default=None,null=True,blank=True,on_delete=models.SET_NULL)
    shop_notes = models.CharField(max_length=255,default="")
    ro_completed = models.DateTimeField(null=True)

class FlagsHistory(models.Model):
    ro = models.ForeignKey(RO)
    flag = models.ForeignKey(Flags)
    notes = models.CharField(max_length=255,null=False,default="")
    created_at = models.DateTimeField(null=False,default=utils.timezone.now)
    created_by = models.ForeignKey(User,null=True,default=None,on_delete=models.SET_NULL)
         
class Notes(models.Model):
    comment = models.CharField(max_length=1024*10,null=False)
    ro = models.ForeignKey(RO,null=False)
    created_at = models.DateTimeField(null=False,default=utils.timezone.now)
    created_by = models.ForeignKey(UserProfile,null=False,)
    current_flag = models.CharField(max_length=10,default="flag1")
    
    
    
class Appointment(models.Model):                            
    customer = models.ForeignKey(UserProfile, null=True, related_name="customerapt",blank=True)
    vehicle = models.ForeignKey(CustomerVehicle,null=True, related_name="vehicleapt",blank=True)
    advisor = models.ForeignKey(User, null=True, related_name="advisorapt",blank=True,on_delete=models.SET_NULL)
    way_away = models.ForeignKey(WayAway, null=True, related_name="wayaway",blank=True)
    appointment_status = models.ForeignKey(AppointmentStatus,default=None, null=True, related_name="aptstatus",blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    confirmation_code = models.CharField(null=True,default="",max_length=2000,blank=True)
    ro = models.ForeignKey(RO, null=True,related_name="ro",blank=True)
    contact_me = models.BooleanField(default=False,blank=True)
    contact_time = models.CharField(max_length=20,default="")
    state_wayaway = models.ForeignKey(States,null=True,default=None)
    driver_liscens_number = models.CharField(max_length=255,null=True,blank=True,default="")
    insurance_company_name = models.CharField(max_length=255,null=True,blank=True,default="")
    insurance_card_number = models.CharField(max_length=255,null=True,blank=True,default="")
    maintenance = models.BooleanField(default=False,blank=True)
    service_notes = models.TextField(max_length=2000,default=None,null=True, blank=True)   
    odometer_reading = models.CharField(max_length=255, null=True , blank=True)
    comments = models.TextField(max_length=2000,default='',null=True)
    dealer = models.ForeignKey(Dealer,blank=True,default=None,null=True)
    checkin_time = models.DateTimeField(null=True,blank=True)
    customer_signatures = models.TextField(null=True , default=None)
    creditcard_id = models.CharField(null=True , max_length= 2000)
    payment_status = models.BooleanField(default=False) 
    payment_id = models.CharField(null=True , max_length=2000)
    reserve_wayaway = models.BooleanField(default=False) 
    appointment_reminder_status = models.BooleanField(default=False)
    appointment_recommandation_status = models.BooleanField(default=False)
    odometer_data = models.TextField(blank=True,null=True,default=True)
    odometer_image = models.ImageField(blank=True,null=True,default=None)
    
class WalkaroundVehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle,null=True)
    dealer = models.ForeignKey(Dealer, null=True)
    image = models.ImageField(null=True , default=None)

class WalkaroundVehicleMap(models.Model):
    vehicleimage = models.ForeignKey(WalkaroundVehicleImage)
    type = models.CharField(max_length=255 , null=True , default=None)
    coords = models.TextField(null=True , default=None)
    name  = models.CharField(max_length=255 , null=True ,default=None)
    
class walkaroundnotes(models.Model):
    appointment = models.ForeignKey(Appointment , null=False)
    type = models.CharField(max_length =255 , null=True)
    notes = models.TextField(null=True)
    image = models.ImageField(null=True,default=None)
    image_name = models.CharField(max_length = 255 , null=True,default=None,blank=True)
    other_category = models.CharField(max_length = 255 , null =True)
    other_type = models.CharField(max_length = 255 , null =True)
    RR = models.ForeignKey(VehicleTireWidth ,null=True , related_name ="RR")
    RF = models.ForeignKey(VehicleTireWidth ,null=True, related_name ="RF")
    LR = models.ForeignKey(VehicleTireWidth ,null=True, related_name ="LR")
    LF = models.ForeignKey(VehicleTireWidth ,null=True, related_name ="LF")
    
class WalkaroundInitials(models.Model):
    appointment = models.ForeignKey(Appointment , null=False)
    type = models.CharField(max_length=255 , null=True)
    initials = models.TextField()
    
class AppointmentService(models.Model):
    appointment = models.ForeignKey(Appointment, null=False, related_name="appointmentservice")
    service = models.ForeignKey(ServiceRepair, null=False, related_name="service")
#     ro_number = models.ForeignKey(RO, null=True,related_name="ro")
    technician = models.ForeignKey(User, null=True,blank=True, related_name="apttechnician",on_delete=models.SET_NULL)
    note = models.TextField(null=True)
    price = models.FloatField(default=0.0)
    desc = models.TextField(null=True,blank=True,default=None)
    
    
    
class AppointmentRecommendation(models.Model):
    INSPECTION_STATUS_CHOICE = (
                                ("Accept",_("Accept")),("Decline",_("Decline"))
                                )
    INSPECTION_RESULT_CHOICE = (
                                ("Fail",_("Fail")),("Success",_("Success"))
                                )
    appointment = models.ForeignKey(Appointment, null=False, related_name="aptrecommendation")
    service = models.ForeignKey(ServiceRepair, null=True,default=None,blank=True, related_name="serrecommendation")
    technician = models.ForeignKey(User, null=True,default=None, related_name="aptrecomtechnician",on_delete=models.SET_NULL)
    status = models.CharField(choices=INSPECTION_STATUS_CHOICE,max_length=10,default="Decline")
    result = models.CharField(choices=INSPECTION_RESULT_CHOICE,max_length=10,default="Fail")
    recommnded_by = models.ForeignKey(User,default=None,blank=True,null=True,on_delete=models.SET_NULL)
    date_advised = models.CharField(max_length=200,default="")
    notes = models.TextField(default="",blank=True)
    price = models.FloatField(default=0.0)
    price_unit =  models.CharField(max_length=10, default = '$')
    labor = models.FloatField(default=0.0)
    parts = models.FloatField(default=0.0)
    
#     ro = models.ForeignKey(RO,null=True,default=None)
    
class InspectionPackage(models.Model):
    dealer= models.ForeignKey(Dealer)
    package = models.CharField(max_length=255,null=False)

class InspectionItems(models.Model):    
    item = models.CharField(max_length=255,null=False)
    
class InspectionCatagories(models.Model):
    category = models.CharField(max_length=50,null=False)
    package = models.ForeignKey(InspectionPackage)
    
class InspectionCategoriesItems(models.Model):
    category = models.ForeignKey(InspectionCatagories)
    item = models.ForeignKey(InspectionItems)
       
class RoInspection(models.Model):
    ro = models.ForeignKey(RO)  
    inspection = models.ForeignKey(InspectionCategoriesItems)
    observation = models.CharField(max_length=100,null=True)
    recommendations = models.CharField(max_length=100,null=True)
    specs = models.CharField(max_length=100,null=True)
    image = models.ImageField(null=True,default=None)
    status = models.CharField(max_length=10,default="pass")
    inspector = models.ForeignKey(User,default=None,blank=True,null=True,on_delete=models.SET_NULL)
    
class EmailTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    template = models.TextField()
    html_template = models.TextField(null=True)
    subject = models.TextField(null=True)
    dealer = models.ForeignKey(Dealer,blank=True,default=None,null=True)
    signature =  models.TextField(null=True)
    
class EmailQueue(models.Model):
        
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(EmailTypes)
    created_time = models.DateTimeField(null=True)
    subject = models.CharField(max_length=255)
    cc = models.TextField(null=True)
    bcc = models.TextField(null=True)
    params = models.TextField(null=True)
    status = models.IntegerField(default=0)
    mail_time = models.DateTimeField(null=True)
    sent_time = models.DateTimeField(null=True)
    mail_error  = models.IntegerField(default=0)
    mail_retries  = models.IntegerField(default=0)
    mail_failuire_date = models.DateTimeField(null=True)
    mail_detail = models.TextField(null=True)
    mail_from = models.TextField(default="")
    mail_to= models.TextField(default="")
    mail_error_detail = models.TextField(null=True)
    dealer = models.ForeignKey(Dealer,blank=True,default=None,null=True)
        
class EmailMultimedia(models.Model):
    id = models.AutoField(primary_key=True)
    multimedia_file = models.CharField(max_length=255)
    dealer = models.ForeignKey(Dealer,blank=True,default=None,null=True)
    
class AdvisorCapacity(models.Model):
    advisor = models.ForeignKey(User, null=False, related_name="advcapacity")  
    shop = models.ForeignKey(Dealer, null=False, related_name="shopcapacity") 
    monday = models.BooleanField(default=True) 
    tuesday = models.BooleanField(default=True) 
    wednesday = models.BooleanField(default=True) 
    thursday = models.BooleanField(default=True) 
    friday = models.BooleanField(default=True) 
    saturday = models.BooleanField(default=True) 
    
class AdvisorRestrictions(models.Model):
    advisor = models.ForeignKey(User, null=False, related_name="advrestriction") 
    monday = models.BooleanField(default=True) 
    tuesday = models.BooleanField(default=True) 
    wednesday = models.BooleanField(default=True) 
    thursday = models.BooleanField(default=True) 
    friday = models.BooleanField(default=True) 
    saturday = models.BooleanField(default=True) 
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    repeat = models.BooleanField(default=True)
    type = models.CharField(max_length=100, null = True)
    
    
    
class ReminderType(models.Model):
    name =   models.CharField(max_length=100)
    description = models.CharField(max_length=20000)
    
    
    
    
class ReminderSettings(models.Model):
#     REMINDER_TYPE = (
#                                 ("SCHEDULE_APPOINTMENT",_("SERVICES")),("MISS_APPOINTMENT",_("PICKUP_READY"))
#                                 )
    
    customer = models.ForeignKey(UserProfile)
    email = models.BooleanField(default=False)
    text = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    type = models.ForeignKey(ReminderType)


class ReportsHistory(models.Model):
    report_name = models.CharField(max_length=255,null=True,default="")
    last_updated_time = models.DateTimeField(null=True)

  
    
def appointment_callback(sender, **kwargs):
    """
            This is a signal which pushes update signals to each client listening
    """
    from dealership.services import userservices  
    instance = kwargs["instance"]
    dealer = None
    try:
        
        service = userservices.UserService()
        if instance.id == None:
            old_instance = None
        else:
            old_instance = Appointment.objects.get(id=instance.id)
        
        pushr = PusherService()
        pushr.connect(settings.CENTRIFUGE_API_URL, settings.CENTRIFUGE_SECRET)
        if old_instance:
            if old_instance.start_time:
                old_instance.start_time = timezone.localtime(old_instance.start_time)
            if old_instance.end_time:
                old_instance.end_time = timezone.localtime(old_instance.end_time)
        if instance.start_time:
            instance.start_time = timezone.localtime(instance.start_time)
        if instance.end_time:
            instance.end_time = timezone.localtime(instance.end_time)
        serialized_obj_old = serializers.serialize('json', [ old_instance, ])
        serialized_obj_new = serializers.serialize('json', [ instance, ])

        if instance.advisor:
            dealer = instance.advisor.userprofile.dealer
            
        if dealer:
            pushr.update_clients(str(dealer.id),
                                    ["appointments"],
                                    {"old_data":
                                       serialized_obj_old,
                                    "new_data":
                                         serialized_obj_new
                                    }
                             )
        print dealer
        print("Request finished!")
    except Exception,e:
        print str(e)
        
        
    
    
    
def appointment_status_email(sender, **kwargs):
    import json
    from django.utils import timezone
    from django.core.urlresolvers import reverse
    from dealership.factories import DealerShipServicesFactory
    from dealership.services import userservices  
    from dealership.services.emailservice import EmailService
    dealer_factory = DealerShipServicesFactory()
    notificationservice = dealer_factory.get_instance("notification")
    appointmentservice = dealer_factory.get_instance("appointment")
    instance = kwargs["instance"]
    try:
        service = userservices.UserService()
        if instance.id == None:
            old_instance = None
        else:
            old_instance = Appointment.objects.get(id=instance.id)
            
        if old_instance.appointment_status_id !=  instance.appointment_status_id:
            customer = instance.customer
            if customer:
                notification_settings = notificationservice.get_schedlued_settings(customer)
                send_text = False
                if notification_settings["text"] == True:
                    send_text=True
                main_site_url = settings.SITE_MAIN_URL+reverse('customer:main')+"?dealer_code=" +instance.dealer.dealer_code
                account_url = settings.SITE_MAIN_URL+reverse('customer:accountsettings')+"?dealer_code=" +instance.dealer.dealer_code
                notification_url = settings.SITE_MAIN_URL+reverse('customer:notifications')+"?dealer_code=" +instance.dealer.dealer_code
                if instance.appointment_status_id == appointmentservice.STATUS_SCHEDULED_ID:
                    app_service = AppointmentService.objects.filter(appointment_id = instance.id)
                    service_name = []
                    for obj in app_service:
                        service_name.append(obj.service.name)
                    instance.start_time = timezone.localtime(instance.start_time)
                    context = {"name" : instance.customer.first_name+" "+instance.customer.last_name , "c_code": instance.confirmation_code , 
                               "start_time": instance.start_time.strftime('%B %d %Y %I:%M %p'),
                               "vehicle" : instance.vehicle.vehicle.make.name+" "+ instance.vehicle.vehicle.model.name , "advisor": instance.advisor.userprofile.first_name+" "+ instance.advisor.userprofile.last_name,
                               "g_cyl": settings.SITE_MAIN_URL+reverse('customer:sync_gcalendar')+"?appointment_id="+str(instance.id)+"&dealer_code="+instance.dealer.dealer_code,
                               "o_cyl": settings.SITE_MAIN_URL+reverse('customer:download_calendar')+"?appointment_id="+str(instance.id)+"&dealer_code="+instance.dealer.dealer_code,
                               "service_name": service_name,"wayaway":instance.way_away.name,
                               "appointment_change_url": settings.SITE_MAIN_URL+reverse('customer:search_by_code_phone')+"?appointment_id="+str(instance.id)+"&dealer_code="+instance.dealer.dealer_code,
                               "main_site_url":main_site_url,
                               "account_url":account_url,
                               "notification_url":notification_url,
                               "dealer_name":instance.dealer.name,
                               "dealer_id":instance.dealer.id,
                               "dealer_address":instance.dealer.address_line1+" "+instance.dealer.address_line2,
                               "dealer_code": instance.dealer.dealer_code}
                    params = json.dumps(context)
                    notificationservice.send_dealer_based_notification(instance.dealer,instance.customer,params,"appointment_schedules",send_email=True,send_text=send_text)
                elif instance.appointment_status_id == appointmentservice.CANCEL_STATUS_ID:
                    instance.start_time = timezone.localtime(instance.start_time)
                    context = {"name" : instance.customer.first_name+" "+instance.customer.last_name,
                               "main_site_url":main_site_url,
                               "account_url":account_url,
                               "notification_url":notification_url,
                               "start_time": instance.start_time.strftime('%B %d %Y %I:%M %p'),
                               "dealer_address":instance.dealer.address_line1+" "+instance.dealer.address_line2
                               }
                    params = json.dumps(context)
                    notificationservice.send_dealer_based_notification(instance.dealer,instance.customer,params,"appointment_cancel",send_email=True,send_text=send_text)
#                 
    except Exception,e:
        print "failed sending email"
        print e
        
def flag_changed(sender, **kwargs):
    import json
    from django.utils import timezone
    from django.core.urlresolvers import reverse
    from dealership.services.emailservice import EmailService
    from dealership.factories import DealerShipServicesFactory
    from dealership.services import userservices  
    dealer_factory = DealerShipServicesFactory()
    notificationservice = dealer_factory.get_instance("notification")
    appointmentservice = dealer_factory.get_instance("appointment")
    instance = kwargs["instance"]
    
    
    try:
        service = userservices.UserService()
        if instance.id == None:
            old_instance = None
        else:
            old_instance = RO.objects.get(id=instance.id)
            
        if old_instance.flag3_id !=  instance.flag3_id and instance.flag3_id !=None and instance.flag3.customer_facing==1:
            app  = Appointment.objects.get(ro=instance.id)
            advisor = app.advisor.userprofile
            main_url = settings.SITE_MAIN_URL
            
            send_text = True
            if advisor:
                notification_settings = notificationservice.get_flagging_settings(advisor)
                if notification_settings.get("text",True) == False:
                    send_text=False
            if advisor:
                context = {"name":app.customer.first_name+" "+app.customer.last_name,"flag_name":instance.flag3.name,"notes":instance.shop_notes,
                           "main_url":main_url+reverse('customer:status_alert_index',kwargs={'appointment_id': app.id})}
                param = json.dumps(context)
                if instance.flag3_id == app.dealer.approval_needed_flag_id and app.dealer.approval_needed_flag_id!=0:
                    notificationservice.send_dealer_based_notification(app.dealer,advisor,param,"approval_required",send_email=True,send_text=send_text)
                    notificationservice.send_dealer_based_notification(app.dealer,app.customer,param,"approval_required",send_email=True,send_text=send_text)
#                    
                elif instance.flag3_id == app.dealer.carwash_flag_id and app.dealer.carwash_flag_id!=0:
                    notificationservice.send_dealer_based_notification(app.dealer,advisor,param,"car_wash",send_email=True,send_text=send_text)
                    notificationservice.send_dealer_based_notification(app.dealer,app.customer,param,"car_wash",send_email=True,send_text=send_text)
                   
                else:
                    notificationservice.send_dealer_based_notification(app.dealer,advisor,param,"flags_change",send_email=True,send_text=send_text)
                    notificationservice.send_dealer_based_notification(app.dealer,app.customer,param,"flags_change",send_email=True,send_text=send_text)
                   
    except Exception,e:
        print "failed sending email"
        print e
        
        
signals.pre_save.connect(appointment_status_email, sender=Appointment)
signals.pre_save.connect(appointment_callback, sender=Appointment)
signals.pre_save.connect(flag_changed, sender=RO)



    