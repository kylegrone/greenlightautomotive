'''
Created on 24-Nov-2015

@author: Shoaib Anwar
'''

from __builtin__ import True
from calendar import Calendar
from datetime import timedelta
import datetime
import json
import math
import time
import uuid

from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db.models import Q
from django.db.models.base import Model
from django.utils import timezone
from django.utils import timezone
from icalendar import Calendar, Event
import pytz

from BMW import settings
from dealership import conf
from dealership.models import CreditCardInfo, Appointment, AppointmentStatus, \
    WayAway, UserProfile, Dealer, RO


class AppointmentService():    
  
  
    
    STATUS_SCHEDULED_ID = 1
    CANCEL_STATUS_ID = 11
    COMPLETED_STATUS_ID = 8
    NO_SHOW_STATUS = 12
    
    
    def setservices(self):
        from customer.factories import CustomerServicesFactory
        from dealership.factories import DealerShipServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.dealer_service_factory = DealerShipServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        self.userservice = self.dealer_service_factory.get_instance("user")        
        self.vehicle_service = self.dealer_service_factory.get_instance("vehicle")
        self.repair_service = self.dealer_service_factory.get_instance("repair")
        self.dealership_service = self.dealer_service_factory.get_instance("dealership")
        self.capacity_service = self.dealer_service_factory.get_instance("capacity")
        self.email_service = self.dealer_service_factory.get_instance("email")
        self.appointment_service = self
     
     
    def update_noshow(self):
        try:
            time_threshold = timezone.now() - timedelta(hours=24)
            
            Appointment.objects.filter(appointment_status_id = self.STATUS_SCHEDULED_ID,start_time__lt=time_threshold).update(appointment_status_id=self.NO_SHOW_STATUS)
        except Exception,e:
            print "error"   
            
            
    def get_calendar(self,appointment_id):
        try:
            appointmet = self.get_appointment(appointment_id)
            if appointmet:
                cal = Calendar()
               
        
                cal.add('prodid', '-//{0} Events Calendar//{1}//'.format("BMW service Appointment",
                                                                        "BMW service Appointment"))
                cal.add('version', '2.0')
        
                ical_event = Event()
                ical_event.add('summary', "Appointment Scheduled with BMW Services")
                ical_event.add('dtstart', appointmet.start_time)
                ical_event.add('dtend', appointmet.start_time+ datetime.timedelta(minutes=20))
                ical_event.add('dtstamp', appointmet.start_time)
                ical_event['uid'] = str(appointmet.confirmation_code)
                cal.add_component(ical_event)
                return cal  
            else:
                return False
            
        except Exception,e:
            print e
            
            return False
    def save_advisor(self,appointment,advisor_id=None):
        try:
            user = None
            if advisor_id:
                    user = User.objects.get(id=advisor_id)
            appointment.advisor = user
            appointment.save()
            return True       
        except Exception,e:
            print e
            return False   
    
    def email_appointment(self,appointment):
        try:
            pass
        except:
            pass
            
    def save_appoitment_with(self,slab_time,advisor_id,way_away_id,profile_id,comments,contact_me,dealer_id=None):
      
        try:
            app  = Appointment()
            if slab_time:
                app.start_time = slab_time
            if advisor_id:
                app.advisor_id = advisor_id
            if way_away_id:
                app.way_away_id = way_away_id
            if profile_id:
                app.customer_id = profile_id
            if dealer_id:
                app.dealer_id = dealer_id
            if comments:
                app.comments = comments
            app.appointment_status_id = self.STATUS_SCHEDULED_ID    
            app.save()
            if contact_me:
                self.contact_me(app, contact_me)
            return app
        except Exception,e:
            print "Exception saving appointment"
            print e
            return False
        
    def get_appointmets_by_confirmation(self,dealer,code):
        try: 
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id)
                                                 , )
            filter_aargs = {"start_time__gt":timezone.now(),
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       "appointment_status_id":self.STATUS_SCHEDULED_ID,
                       "confirmation_code" : code
                      }
            ex_filter_args ={}
            exclude_args= ( Q(appointment_status_id=self.CANCEL_STATUS_ID) 
                                                    | Q(appointment_status_id=self.COMPLETED_STATUS_ID)
                                                    |Q(appointment_status_id=None)
                                                    , )
            appointment = Appointment.objects.filter(*args,**filter_aargs
                                               )
            appointment.exclude(*exclude_args,**ex_filter_args)
            return appointment
        except Exception,e:
            print e
            return None
      
      
        
        
    def get_appointmets_by_profile(self,dealer,profile):
        try: 
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id)
                                                  ,)
            filter_aargs = {"start_time__gt":timezone.now(),
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       "appointment_status_id":self.STATUS_SCHEDULED_ID,
                       "customer" : profile
                      }
            ex_filter_args ={}
            exclude_args= ( Q(appointment_status_id=self.CANCEL_STATUS_ID) 
                                                    | Q(appointment_status_id=self.COMPLETED_STATUS_ID)
                                                    |Q(appointment_status_id=None)
                                                    , )
            appointment = Appointment.objects.filter(*args,**filter_aargs
                                                )
            appointment.exclude(*exclude_args,**ex_filter_args)
            return appointment
        except Exception,e:
            print e
            return None  
        
        
        
    def get_appointments_by_phone(self,dealer,phone):
        try:
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id)
                    ,)
            
            filter_aargs = {"start_time__gt":timezone.now(),
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       "appointment_status_id":self.STATUS_SCHEDULED_ID
                      }
            
            if phone:
                args= ( Q(customer__active_phone_number=phone) 
                                                    |Q(customer__phone_number_1=phone)
                                                    |Q(customer__phone_number_2=phone)
                                                    |Q(customer__phone_number_3=phone),Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id), )
            
                
            ex_filter_args ={}
            exclude_args= ( Q(appointment_status_id=self.CANCEL_STATUS_ID) 
                                                    | Q(appointment_status_id=self.COMPLETED_STATUS_ID)
                                                    |Q(appointment_status_id=None)
                                                    , )
            appointment = Appointment.objects.filter(*args,**filter_aargs
                                                )
            appointment.exclude(*exclude_args,**ex_filter_args)
            return appointment
        except Exception,e:
            print e
            return []  
        
              
    def contact_me(self,appoinment,contactme_time = "Any Time"):
        try:
            appoinment.contact_me = True
            appoinment.contact_time = contactme_time
            appoinment.save()
            return True
        except Exception,e:
            return False  
        
    def isbooked(self,appointment):
        if appointment and appointment.appointment_status_id == self.STATUS_SCHEDULED_ID:
            return True
        
        return False
    
    def book_appointment_with_id(self, appointment_id, dealer_id):
        appointment = Appointment.objects.get(id = appointment_id)
        if not self.isbooked(appointment):
            dealer = Dealer.objects.get(id = dealer_id)
            self.book_appointment(appointment, "", dealer)
        return {"appointment_id":appointment_id}         
    
    
    
    def book_appointment(self,appointment,comments="",dealer=None):
        self.setservices()
        try:
            appointment.appointment_status_id = self.STATUS_SCHEDULED_ID
            appointment.confirmation_code = appointment.start_time.strftime('%m%d')+str(appointment.id)
#             appointment.confirmation_code = uuid.uuid4()            
            appointment.comments = comments
            if not appointment.advisor_id and dealer!=None:
                    advisors = self.cuserservice.get_all_available_advisor_for(dealer.dealer_code,appointment)
                    appointment.advisor_id = advisors[0]["id"]
            if dealer:
                appointment.dealer = dealer
#             ro = RO()
#             ro.inspector =  appointment.advisor
#             ro.save()
#             appointment.ro = ro
            appointment.save()
            return True
        except Exception,e:
            print e
            return True
        
    def save_profile(self,appointment,profile):
        try:
            appointment.customer = profile
            appointment.save()
            return True
        except Exception,e:
            print e
            return False
        
    def get_appointmet_by_confirmation(self,dealer,code):
        try: 
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id)
                                               ,   )
            filter_aargs = {"start_time__gt":timezone.now(),
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       "appointment_status_id":self.STATUS_SCHEDULED_ID,
                       "confirmation_code" : code
                      }
            appointment = Appointment.objects.get(*args,**filter_aargs
                                                )
            return appointment
        except Exception,e:
            print e
            return None
        
    def get_appointment_by_phone(self,dealer,phone):
        try:
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id)
                                                ,  )
            
            filter_aargs = {"start_time__gt":timezone.now(),
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       "appointment_status_id":self.STATUS_SCHEDULED_ID
                      }
            
            if phone:
                
                args= ( Q(customer__active_phone_number=phone) 
                                                    |Q(customer__phone_number_1=phone)
                                                    |Q(customer__phone_number_2=phone)
                                                    |Q(customer__phone_number_3=phone), Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id)
                                                  , )
            
                
            
            appointment = Appointment.objects.filter(*args,**filter_aargs
                                                )
            return appointment
        except Exception,e:
            print e
            return []  
        
    def get_appointment_services_values(self,appointment):
        try:
            services = appointment.appointmentservice.values('id',
                                       'service__name',
                                       'note',
                                       'service__dms_opcode',
                                       'service__duration',
                                       'service__price',
                                       'service__price_unit',
                                       'service__description',
                                       'service__image',
                                      )
            return services
        except Exception,e:
            print e
            return None
            
        
    def get_active_appointment_by(self,vehicle_id,dealer):
        try:
            filters = {
                        "vehicle_id":vehicle_id,
                        "start_time__gt":timezone.now(),
#                                             "advisor__userprofile__dealer_id ": dealer.id,
                        "appointment_status_id":self.STATUS_SCHEDULED_ID
                      }
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                    | Q(dealer_id=dealer.id),
                    )
            appt =  Appointment.objects.filter(*args,**filters).order_by("start_time")
            if appt:
                return appt[0]
            else:
                return None
        except Exception,e:
            print e
            return None 
        
    def get_old_appointments_by(self,vehicle_id,dealer):
        try:
            filters = {
                        "vehicle_id":vehicle_id,
                        "start_time__lt":timezone.now(),
#                         "appointment_status_id":self.STATUS_SCHEDULED_ID
                      }
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                    | Q(dealer_id=dealer.id),
                    )
            appt =  Appointment.objects.filter(*args,**filters).order_by("start_time")
            exclude_args= (  Q(appointment_status_id=self.STATUS_SCHEDULED_ID)
                            |Q(appointment_status_id=None)
                             , )
            exclude_kargs  = {}
            appt = appt.exclude(*exclude_args,**exclude_kargs)
            appt=appt.order_by("-start_time")
#             appt.exclude(appointment_status_id_in=[None,self.STATUS_SCHEDULED_ID])
            return appt
        except Exception,e:
            print e
            return None
        
    
    def get_active_appointments_pending_reminder(self):
        try:
            appts  = self.get_active_appointments()
            if appts:
                appts = appts.filter(appointment_reminder_status = False)
            return appts
        except Exception,e:
            return None
            
            
    def get_active_appointments(self):
        try:
            filters = {
                       
                        "start_time__gt":timezone.now(),
#                                             "advisor__userprofile__dealer_id ": dealer.id,
                        "appointment_status_id":self.STATUS_SCHEDULED_ID
                      }
            args = (
                    )
            appts =  Appointment.objects.filter(*args,**filters).order_by("start_time")
            if appts:
                return appts
            else:
                return None
        except Exception,e:
            print e
            return None 
        
    def get_inprogress_appointment_by(self,vehicle_id,dealer):
        try:
            filters = {
                        "vehicle_id":vehicle_id,
                      }
            
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                    | Q(dealer_id=dealer.id),
                    )
            appt =  Appointment.objects.filter(*args,**filters).order_by("start_time")
            if appt:
                exclude_args= ( Q(appointment_status_id=self.CANCEL_STATUS_ID) 
                                                    |Q(appointment_status_id=self.STATUS_SCHEDULED_ID)
                                                    |Q(appointment_status_id=self.COMPLETED_STATUS_ID)
                                                    |Q(appointment_status_id=None)
                                                    , )
                exclude_kargs  = {}
                appt = appt.exclude(*exclude_args,**exclude_kargs)
                return appt[0]
            else:
                return None
        except Exception,e:
            print e
            return None    
        
    def get_active_appointment_by_time(self,slab_time,dealer,advisor=None,exclude_appontment=None):
        try:
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id),
                                                  )
            
            filter_aargs = {"start_time":slab_time,
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       #"appointment_status_id":self.STATUS_SCHEDULED_ID,
                      }
            if advisor:
                filter_aargs['advisor'] = advisor
            
            if filter_aargs.get('advisor')==None and exclude_appontment!=None and exclude_appontment.advisor!=None:
                filter_aargs['advisor'] = exclude_appontment.advisor
                
                
            exclude_args= ( Q(appointment_status_id=None) 
                                                    |Q(appointment_status_id=self.CANCEL_STATUS_ID)
                                                    
                                                    , )
            if exclude_appontment:
                exclude_args= ( Q(appointment_status_id=None) 
                                                    |Q(appointment_status_id=self.CANCEL_STATUS_ID)
                                                    |Q(id=exclude_appontment.id)
                                                    , ) 
                
            
            appts = Appointment.objects.filter(*args,**filter_aargs
                                                ).exclude(*exclude_args)
#         
            
            if appts:
                return appts
            else:
                return []
        except Exception,e:
            print e
            return None 
    
    
    def get_active_appointment_by_date(self,slab_time,dealer,advisor=None,exclude_appontment=None):
        try:
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id),
                                                  )
            
            start_time = slab_time.replace(hour=0, minute=0, second=0)
            end_time = slab_time.replace(hour=23, minute=59, second=0)
            filter_aargs = {"start_time__gte":start_time,
                            "start_time__lte":end_time,
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       #"appointment_status_id":self.STATUS_SCHEDULED_ID,
                      }
          
            if advisor:
                filter_aargs['advisor'] = advisor
            
            if filter_aargs.get('advisor')==None and exclude_appontment!=None and exclude_appontment.advisor!=None:
                filter_aargs['advisor'] = exclude_appontment.advisor
                
                
            exclude_args= ( Q(appointment_status_id=None) 
                                                    |Q(appointment_status_id=self.CANCEL_STATUS_ID)
                                                    
                                                    , )
            if exclude_appontment:
                exclude_args= ( Q(appointment_status_id=None) 
                                                    |Q(appointment_status_id=self.CANCEL_STATUS_ID)
                                                    |Q(id=exclude_appontment.id)
                                                    , ) 
                
            
            appts = Appointment.objects.filter(*args,**filter_aargs
                                                ).exclude(*exclude_args)
#         
            
            if appts:
                return appts
            else:
                return []
        except Exception,e:
            print e
            return None 
    
    def cancel_appointment(self,id):
        try:
            app =Appointment.objects.get(id=id)
            app.appointment_status_id = self.CANCEL_STATUS_ID
            app.save()
        except Exception,e:
            print e
            pass
            
    
    def get_appointment(self,id):
        try:
            app =Appointment.objects.get(id=id)
            return app
        except Exception,e:
            print e
            return None
        
    def get_active_appointment(self,id):
        """
            get active scheduled appointment
        """
        try:
            app =Appointment.objects.get(id=id, start_time__gt=timezone.now(),
                                               appointment_status_id=self.STATUS_SCHEDULED_ID)
            return app
        except Exception,e:
            print e
            return None   
        
        
    def get_valid_appointment(self,id):
        """
            this is to get appointment that is schedules or waiting to be booked
        """
        try:
            app =Appointment.objects.get(Q(start_time__gte=timezone.now) 
                                                    |Q(start_time=None)
                                                    ,id=id)#,start_time__gte=timezone.now)
            if app.appointment_status_id == None or app.appointment_status_id ==self.STATUS_SCHEDULED_ID :
                return app
            return None
        except Exception,e:
            print e
            return None   
        
        
    def save_empty_appointment(self,dealer_id=None):
        try:
            app = Appointment()
            if dealer_id:
                app.dealer_id = dealer_id
            app.save()
            return app
        except Exception,e:
            print e
            return None
        
    def save_customer_vehicle(self,appt,vehcile_id):
        try:
            appt.vehicle_id =   vehcile_id
            appt.save()
            return True
        except Exception,e:
            print e
            return False
    
        
    
    def find_by_confirmation_phone(self,dealer,code=None,liscense_number=None,vin_number=None,make=None,model=None):
        try:
            
            args = (Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id),
                    )
            
            filter_aargs = {
                            "start_time__gt":timezone.now(),
#                       "advisor__userprofile__dealer__id" : dealer.id,
                       "appointment_status_id":self.STATUS_SCHEDULED_ID
                      }
            
            if code:
                
                args= ( Q(confirmation_code=code) 
                                                    |Q(customer__phone_number_1=code)
                                                    |Q(customer__phone_number_2=code)
                                                    |Q(customer__phone_number_3=code)
                                                    |Q(customer__active_phone_number=code) 
                                                    ,
                                                     Q(advisor__userprofile__dealer__id=dealer.id) 
                                                    | Q(dealer_id=dealer.id)
                    
                                                     )
            if liscense_number:
                filter_aargs["vehicle__lisence_number"] = liscense_number
               
                
                
            if vin_number:
                filter_aargs["vehicle__vin_number"] = vin_number
                
            if make and model:
                filter_aargs["vehicle__vehicle__make__val"] = make
                filter_aargs["vehicle__vehicle__model__val"] = model
                
            appointment = Appointment.objects.filter(*args,**filter_aargs
                                                )
            return appointment
        except Exception,e:
            print e
            return None
        
        
    def get_appointments_wallboard_data(self, dealer_id, date_string = None):
        
        self.setservices()
        data = {}  
        try:
            if date_string == None:
                now = timezone.now()  
            else: 
                now = datetime.datetime.strptime(date_string, '%Y-%m-%d')
                now = timezone.make_aware(now)
                
                
                
            timings = self.dealership_service.get_dealer_shop_time(now, dealer_id)
             
            status = {} 
            wayaway = {}   
            status_list =  list(AppointmentStatus.objects.all().values());
            wayaway_list = list(WayAway.objects.all().values());
    
            for st in status_list:
                key = st['name'].lower().replace (" ", "_")
                status[st['id']] = key
                data[key] = 0
                
            for st in wayaway_list:
                key = st['name'].lower().replace (" ", "_")
                wayaway[st['id']] = key
                data[key] = 0
                
            data['arrived_greeted'] = 0
            data['notarrived'] = 0
            data['other'] = 0
                
            status_count = Appointment.objects.values("appointment_status_id").order_by().annotate(Count('appointment_status_id')).filter(start_time__range=[timings['open_time'], timings['close_time']],dealer_id = dealer_id).exclude(appointment_status_id=None)
            
            for apt in status_count:
                if apt.get('appointment_status_id'):
                    data[status[apt['appointment_status_id']]] = apt.get('appointment_status_id__count',0)
            
            data['arrived_greeted'] = data.get('arrived',0) + data.get('greeted',0) 
            
            not_arrived = list(Appointment.objects.filter(appointment_status_id = self.STATUS_SCHEDULED_ID, start_time__range=[timings['open_time'], timezone.now()],dealer_id = dealer_id).values())
            data['notarrived'] = len(not_arrived)  
            
            wayaway_count = Appointment.objects.values("way_away_id").order_by().annotate(Count('way_away_id')).filter(start_time__range=[timings['open_time'], timings['close_time']],dealer_id = dealer_id).exclude(appointment_status_id=None)
            for apt in wayaway_count:
                if apt.get('way_away_id'):
                    data[wayaway[apt['way_away_id']]] = apt.get('way_away_id__count',0)    
    
            data['other'] = data.get('uber',0) + data.get('shuttle',0) + data.get('drop_off',0)
        except Exception as ex:
            
            self.email_service.send_exception("dealership", 
                                            "appointmentservice", 
                                            "get_appointments_wallboard_data", 
                                            str(ex));
        return data 

    """
    get_appoiontments_by_time
     * get all the appointments for a particular day categorized in time slabs
    """
    def get_appoiontments_by_time(self, datetime_string, dealer_id, advisor_id = None):
        self.setservices()
        #pytz.timezone(settings.TIME_ZONE).localize(datetime_string)        
        now = timezone.now()        
        slab = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
        slab = timezone.make_aware(slab)
        slab_up = slab + datetime.timedelta(minutes = 19)
        args = ()
        filter_aargs = {"start_time__range":[slab, slab_up],
                            "dealer_id" : dealer_id,
                            "customer_id__isnull":False,
                            "appointment_status_id__isnull":False
                      }         
        #appointments = Appointment.objects.filter(start_time__range=, dealer_id = dealer_id, advisor_id = advisor_id, customer_id__isnull = False,appointment_status_id__isnull=False)
        if advisor_id:
            filter_aargs["advisor_id"] = advisor_id          
         
        appointments = Appointment.objects.filter(*args,**filter_aargs
                                                )        
        
        capacity = self.capacity_service.get_capacity_for_slab(slab, dealer_id)
        result = self.format_appointments_data(slab.time().strftime('%I:%M %p'), capacity, appointments)
       
        return {'slab' : result}
    
    def get_appointments_by_advisor(self, date_string, dealer_id, advisor_id): 
        #pytz.timezone(settings.TIME_ZONE).localize(date_string)
        self.setservices()
        timings = self.dealership_service.get_dealer_shop_time(datetime.datetime.strptime(date_string, '%Y-%m-%d'), dealer_id)
        ##start_date_start = datetime.datetime(int(year), int(month), int(day), 00, 00, 00)  
        #start_date_end = datetime.datetime(int(year), int(month), int(day), 23, 59, 59)                   
        appointments = Appointment.objects.filter(start_time__range=[timings['open_time'], timings['close_time']], advisor_id=advisor_id) 
        advisor = User.objects.get(id = advisor_id);
        title = "%s %s" % (advisor.userprofile.first_name, advisor.userprofile.last_name)
        result = self.format_appointments_data(title, 0, appointments)
        return {'slab' : result}
    
    def get_appointments_by_status(self, date_string, dealer_id, status_id):  
        self.setservices()
        #pytz.timezone(settings.TIME_ZONE).localize(date_string)
        timings = self.dealership_service.get_dealer_shop_time(datetime.datetime.strptime(date_string, '%Y-%m-%d'), dealer_id)
        #start_date_start = datetime.datetime(int(year), int(month), int(day), 00, 00, 00)  
        #start_date_end = datetime.datetime(int(year), int(month), int(day), 23, 59, 59)                    
        try:
            
            
            appointments = Appointment.objects.filter(start_time__range=[timings['open_time'], timings['close_time']], appointment_status=status_id) 
            
            status = AppointmentStatus.objects.get(id = status_id);
            result = self.format_appointments_data(status.name, 0, appointments)
            return {'slab' : result} 
        except Exception, e:
            return {'slab' : []}   
    
    def get_appointments_by_time_criteria(self, date_string, dealer_id, search, criteria):
        self.setservices()
        timings = self.dealership_service.get_dealer_shop_time(datetime.datetime.strptime(date_string, '%Y-%m-%d'), dealer_id)
        #start_date_start = datetime.datetime(int(year), int(month), int(day), conf.DEALER_SHOP_OPENING_HOUR, conf.DEALER_SHOP_OPENING_MINUTE, 00)  
        #start_date_end = datetime.datetime(int(year), int(month), int(day), conf.DEALER_SHOP_CLOSING_HOUR, conf.DEALER_SHOP_OPENING_MINUTE, 59) 
        if timings:
            result = self.appointment_search_handler(search, criteria, timings['open_time'], timings['close_time'])
        else:
            result = self.appointment_search_handler(search, criteria)
        return result  

    def get_appointments_by_time_id(self, id, dealer_id):  
        self.setservices() 
        appointments = Appointment.objects.filter(id=id)
        pointer = ""
        id = ""
        data = []
        slabs = []
        for appointment in appointments:
            appointment.start_time = timezone.localtime(appointment.start_time)
            slab_time = self.round_time(appointment.start_time + datetime.timedelta(minutes = 1), 10)
            
            title = slab_time.time().strftime('%I:%M %p')
                  
            if pointer == "":
                pointer = title 
                id = slab_time.strftime('%Y_%m_%d_%I_%M')
            if title != pointer: 
                capacity = self.capacity_service.get_capacity_for_slab(slab_time, dealer_id)
                slab = self.general_appointment_wraper(pointer, capacity, data)
                slab['id'] = id
                slabs.append(slab)
                id = slab_time.strftime('%Y_%m_%d_%I_%M')
                data = []
                pointer = title  
             
            row = self.make_appointment_data(appointment)
            data.append(row)
             
        slab = self.general_appointment_wraper(pointer, 0, data)
        slab['id'] = id
        slabs.append(slab)
                  
        return {'slabs':slabs}  
    
    def appointments_search_by_name(self, criteria, start_date_start, start_date_end):
        if start_date_start == None:
            appointments = None
        else:
            appointments = Appointment.objects.filter(Q(customer__first_name__icontains = criteria) |  Q(customer__last_name__icontains = criteria),   start_time__range=[start_date_start, start_date_end]).order_by('start_time')
        customers = UserProfile.objects.filter(Q(first_name__icontains = criteria) |  Q(last_name__icontains = criteria)).order_by('first_name')
        return self.appointments_search_format_result(appointments, customers)   
     
    def appointments_search_by_phone(self, criteria, start_date_start, start_date_end):
        criteria = criteria.replace ("-", "")
        if start_date_start == None:
            appointments = None
        else:
            appointments = Appointment.objects.filter(Q(customer__phone_number_1__contains = criteria) |  Q(customer__phone_number_2__contains = criteria) | Q(customer__phone_number_3__contains = criteria), start_time__range=[start_date_start, start_date_end]).order_by('start_time')
        customers = UserProfile.objects.filter(Q(phone_number_1__contains = criteria) |  Q(phone_number_2__contains = criteria) | Q(phone_number_3__contains = criteria)).order_by('first_name')
        return self.appointments_search_format_result(appointments, customers)
    
    def appointments_search_by_email(self, criteria, start_date_start, start_date_end):
        if start_date_start == None:
            appointments = None
        else:
            appointments = Appointment.objects.filter(Q(customer__email_1__icontains = criteria) | Q(customer__email_2__icontains = criteria), start_time__range=[start_date_start, start_date_end])
        customers = UserProfile.objects.filter(Q(email_1__icontains = criteria) | Q(email_2__icontains = criteria))
        return self.appointments_search_format_result(appointments, customers)
    
    def appointments_search_by_vin(self, criteria, start_date_start, start_date_end):
        if start_date_start == None:
            appointments = None
        else:
            appointments = Appointment.objects.filter(vehicle__vin_number__icontains = criteria, start_time__range=[start_date_start, start_date_end])
        customers = UserProfile.objects.filter(customervehicle__vin_number__icontains = criteria)
        return self.appointments_search_format_result(appointments, customers)
    
    def appointments_search_by_appt(self, criteria, start_date_start, start_date_end):
        if start_date_start == None:
            appointments = None
        else:
            appointments = Appointment.objects.filter(confirmation_code__icontains = criteria, start_time__range=[start_date_start, start_date_end])
        customers = []
        return self.appointments_search_format_result(appointments, customers)  
    
    def appointments_search_format_result(self, appointments, customers):
        if appointments:
            return {"type":"appointment", "data":appointments[0].id, "url":reverse('dealership:appointment')+"?appointment_id="+str(appointments[0].id)}
        elif customers:
            data = []
            for cust in customers:
                data.append(cust.id)
            if len(data) == 1:
                return {"type":"customer", "data":data, "url":reverse('dealership:appointment')+"?panel=customer&customer_id="+str(data[0])}
            else:
                return {"type":"customer", "data":data, "url":reverse('dealership:customers')+'?customer_id='+json.dumps(data).replace(" ", "")[1:-1]}
        else:
            return {"type":"error"}  
    
    def appointment_search_handler(self, by, criteria, start_date_start = None, start_date_end = None):
        if by == "name":
            appointments = self.appointments_search_by_name(criteria, start_date_start, start_date_end)
        elif by == "phone":
            appointments = self.appointments_search_by_phone(criteria, start_date_start, start_date_end)
        elif by == "email":
            appointments = self.appointments_search_by_email(criteria, start_date_start, start_date_end)
        elif by == "vin":
            appointments = self.appointments_search_by_vin(criteria, start_date_start, start_date_end)
        elif by == "appt":
            appointments = self.appointments_search_by_appt(criteria, start_date_start, start_date_end)
        
        return appointments
#         switcher = {
#             "name":  self.appointments_search_by_name(criteria, start_date_start, start_date_end),
#             "phone": self.appointments_search_by_phone(criteria, start_date_start, start_date_end),
#             "email": self.appointments_search_by_email(criteria, start_date_start, start_date_end),
#             "vin": self.appointments_search_by_vin(criteria, start_date_start, start_date_end),
#             "appt": self.appointments_search_by_appt(criteria, start_date_start, start_date_end)
#         }
#         method = switcher[by]
#         # Call the method as we return it
#         return method
    
    
        
    def get_appointment_by_id(self, id):
        appointment = Appointment.objects.get(id = id) 
        row = self.make_appointment_data(appointment)
        return row   
    
    
    
    def create_update_appointment(self, data,dealer_id=None):
        appointment = Appointment()
        if 'id' in data:
            appointment = Appointment.objects.get(id = data['id']) 
            del data['id']
        for k, v in data.iteritems():    
            #appointment.__dict__[k] = v
            appointment.__setattr__(k, v)
        if dealer_id:
            appointment.dealer_id = dealer_id
        appointment.save()        
        return {"id": appointment.pk}
            
    #TODO: better do it in user
    def get_appointments_advisor(self, dealer_id, datetime_string=None):
        
        self.setservices()
        data = self.userservice.get_dealers_advisors(dealer_id, datetime_string); 
        return data
    
    def get_appointments_status(self, date = None):
        status = AppointmentStatus.objects.all()
        data = []
        for st in status:
            data.append({'id':st.id, 'title':st.name , 'size':1, 'capacity':2}) 
        return {'data':data}
    
    def get_wayaway(self, date = None):
        status = WayAway.objects.all()
        data = []
        for st in status:
            data.append({'id':st.id, 'title':st.name , 'size':1, 'capacity':2}) 
        return {'data':data}
            
        #status = {'title':'status', 'size':1, 'capacity':2}
        #return status
    
    def get_appointments_day(self, date_string, dealer_id, type):
        weekday = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        day = weekday.strftime('%A %b %d')
        slabs = []
        self.setservices()
        timings = self.dealership_service.get_dealer_shop_time(datetime.datetime.strptime(date_string, '%Y-%m-%d'), dealer_id)
        availed = len(list(Appointment.objects.filter(start_time__range=[timings['open_time'], timings['close_time']], dealer_id=dealer_id).values()))
        
        if type == "advisor":
            advisors = self.userservice.get_dealers_advisors(dealer_id);
            for advisor in advisors:
                appointments = Appointment.objects.filter(start_time__range=[timings['open_time'], timings['close_time']], advisor_id=advisor['id']) 
                result = self.format_appointments_data(advisor['title'], 0, appointments)
                result['slab_id'] = "weekly_slab_"+weekday.strftime('%Y_%m_%d_')+str(advisor['id']);
                slabs.append(result)            
        elif type == "status":
            status = AppointmentStatus.objects.all()
            for st in status:
                appointments = Appointment.objects.filter(start_time__range=[timings['open_time'], timings['close_time']], appointment_status=st.id, dealer_id=dealer_id) 
                result = self.format_appointments_data(st.name, 0, appointments)
                result['slab_id'] = "weekly_slab_"+weekday.strftime('%Y_%m_%d_')+str(st.id);
                slabs.append(result) 
        else:
            slab = timings["open_time"]        
            while slab < timings["close_time"]:       
                slab_up = slab + datetime.timedelta(minutes = timings["slot"]-1)
                appointments = Appointment.objects.filter(start_time__range=[slab, slab_up])
                capacity = self.capacity_service.get_capacity_for_slab(slab, dealer_id)
                result = self.format_appointments_data(slab.time().strftime('%I:%M %p'), capacity, appointments) 
                result['slab_id'] = "time_weekly_slab_"+slab.strftime('%Y_%m_%d_%H_%M');
              
                slabs.append(result)
                slab = slab + datetime.timedelta(minutes = timings["slot"])
        
        return {'day':day, 'availed':availed, 'slabs':slabs}
    
    """
    get_weekly_time_grid
     * apt_id is optional
     * takes year, month and start day of the week
     * loops till the 6th day of week and within each loop loops between shop opening and closing timings
     * get the capacity of each appointment slab
     * return data for template
    """
    def get_weekly_time_grid(self, appt_id, date_string, dealer_id):
        
        self.setservices()
#         today = timezone.localtime(timezone.now())
        today = timezone.now()
        dealer = self.dealership_service.get_dealer_by_id(dealer_id)
        current = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        current = timezone.make_aware(current)
        
        data = []           
         
        for i in range(1, 7):   
            next = current + datetime.timedelta(days = 1)  
            timings = self.dealership_service.get_dealer_shop_time(current, dealer_id) 
            slab_start = timings['open_time']   
            day_data = []                        
            appointments = Appointment.objects.values("start_time").order_by().annotate(Count('start_time')).filter(start_time__range=[current, next])
            current_appointment = Appointment.objects.get(id = appt_id)                 
            while(slab_start < timings['close_time']):
                slab_end = slab_start + datetime.timedelta(minutes = (timings['slot'] - 1))
                css_class = ""
                css_btn = "default"
                
                if slab_start < today:
                    css_class = "disabled"
                else:
#                     slab_apt = appointments.filter(start_time__range=[slab_start, slab_end])
                    if self.capacity_service.check_slab_availibity(slab_start,dealer,current_appointment)==False:
                        css_class = "disabled"
#                     if slab_apt:   
#                         if slab_apt[0]['start_time__count'] == slab_capacity:
#                             css_class = "disabled"

                            
                if current_appointment.start_time == slab_start:                       
                    css_btn = "success"
                day_data.append({'title':slab_start.strftime('%I:%M %p'),
                                 #'start_time':slab_start.strftime('%b. %d, %Y, %I:%M %p'), 
                                 'start_time':slab_start.strftime('%Y-%m-%d %H:%M'),
                                 'class':css_class, 
                                 'btn':css_btn})
                slab_start = slab_start + datetime.timedelta(minutes = timings['slot']) 
            data.append({'title':current.strftime('%A %m/%d') , 'data':day_data})   
            current =  next
                 
        return data
        
    """
    format_appointments_data
     * get all the appointments and extract data
    """        
    def format_appointments_data(self, title, capacity, appointments):
        data = []
        for appointment in appointments:
            row = self.make_appointment_data(appointment)
            data.append(row)
        
        result = self.general_appointment_wraper(title, capacity, data)
        return result  
    
    def general_appointment_wraper(self, title, capacity, data):
        size = data.__len__() 
        if capacity == 0:
            color = "GridRowBlue"
        else:   
            half_capacity = capacity/2
            color = "GridRowGreen"
            if (size >= capacity):
                color = "GridRowRed"
            elif(size >= half_capacity):
                color = "GridRowYellow"        
         
        result = {'data':data, 'color':color, 'size':size, 'capacity': capacity, 'title': title}
        return result
    
    def make_appointment_data(self, apt):
        self.setservices()
        user = UserProfile.objects.get(id= apt.customer_id)
        status = AppointmentStatus.objects.get(id = apt.appointment_status_id)
        time_left = {'min' : 0 , 'sec': 0}
        if status.name =="In Progress":
            time_left = self.get_in_progress_remaining_time(apt.checkin_time) 
        apt.start_time = timezone.localtime(apt.start_time)
        row = {"id":apt.id,
               "appointment":apt,
               "time": apt.start_time.time().strftime('%I:%M %p'),
               "time2" : apt.start_time.strftime('%A %b %d, %I:%M %p'),
               "datetime": apt.start_time.strftime('%Y-%m-%d %H:%M'),
               "customer":self.userservice.get_customer_detail(apt.customer_id),
               "creditcard": {},
               "vehicle": {},               
               "service": self.repair_service.get_appointment_services(apt.id),
               "wayaway": "",
               "advisor": self.cuserservice.get_user_name(apt.advisor_id),
               "status": "%s" % (status.name),
               "insurence" : self.cuserservice.get_user_driver_insurance(user),
               "time_left" : time_left,
               }
        
        try:
            row['creditcard'] = {'crdtcard' :self.cuserservice.get_cc_profile(user),
                          'cardtypes' : CreditCardInfo._meta.get_field('card_type').choices,
                          'cardexpyr' : CreditCardInfo._meta.get_field('card_exp_year').choices ,
                          'cardexpmonth' : CreditCardInfo._meta.get_field('card_exp_month').choices},
        except Exception, ex:
            pass    
        
        try:
            row['vehicle'] = self.vehicle_service.get_vehicle_appointment_data(apt.vehicle_id)
        except Exception, ex:
            print ex
            pass
        
        try:
            wayaway = WayAway.objects.get(id = apt.way_away_id)
            row["wayaway"] = wayaway.name
        except Exception, ex:
            pass
        
        return row
        
    def round_time(self, tm, points):
        upmins = math.ceil(float(tm.minute)/10)*10
        diffmins = upmins - tm.minute - points
        newtime = tm + datetime.timedelta(minutes=diffmins)
        newtime = newtime.replace(second=0)
    
        return newtime
    
    def get_in_progress_remaining_time(self,date_time):
        try:
            checkin_time = date_time + datetime.timedelta(minutes = 5)
            current_time = timezone.now()
            if current_time > checkin_time:
                return {'min' : 0 , 'sec': 0}
            else:
                remaining_time = checkin_time - current_time
                return {'min':remaining_time.seconds / 60 ,'sec' : remaining_time.seconds%60 }
        except Exception as ex:
            self.email_service.send_exception("dealership", 
                                              "appointmentservice", 
                                              "get_in_progress_remaining_time", 
                                              str(ex));
        
    def get_customer_secheduled_appointments_for_dealer(self,customer_id, dealer_id):             
        args = ()
        filter_aargs = {"start_time__gt":timezone.now(),
                            "dealer_id" : dealer_id,
                            "customer_id":customer_id,
                            "appointment_status_id":self.STATUS_SCHEDULED_ID
                      }    
        appointment = Appointment.objects.filter(*args,**filter_aargs
                                                )
        return appointment
