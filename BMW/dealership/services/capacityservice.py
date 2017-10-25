from __builtin__ import False, True
from datetime import timedelta
import datetime
from functools import wraps
import test
import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils import timezone
from django.utils.decorators import available_attrs

from BMW import settings
from dealership.models import AdvisorCapacity, AdvisorRestrictions, \
    CapacityCounts


class CapacityService():
    
    def setservices(self):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        from dealership.factories import DealerShipServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.dealer_service_factory = DealerShipServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        self.userservice = self.dealer_service_factory.get_instance("user")
        self.appointment_service = self.dealer_service_factory.get_instance("appointment")
        self.vehicle_service = self
        self.repair_service = self.dealer_service_factory.get_instance("repair")
        self.dealership_service = self.dealer_service_factory.get_instance("dealership")
     
     
    def get_available_slabs_for(self,slab_day,dealer,advisor=None):
        
        self.setservices()
        timings = self.dealership_service.get_dealer_shop_time(slab_day, dealer.id)
        now = timezone.now()
        available_slabs = []
        if timings:
            slab = timings["open_time"]  
            while slab < timings["close_time"]:
                slab_time_obj = slab_day.strftime('%Y-%m-%d ')+slab.time().strftime('%H:%M')
                slab_time_obj = timezone.make_aware(datetime.datetime.strptime(slab_time_obj, '%Y-%m-%d %H:%M'))
                if slab_time_obj > now:
                    slab_detail = {"value":slab_day.strftime('%Y-%m-%d ')+slab.time().strftime('%H:%M'),"name":slab_day.strftime('%a %b %d, ')+slab.time().strftime('%I:%M %p')}
                    if self.check_slab_availibity(slab, dealer,None ):
                        if advisor:
                                if self.check_slab_for_advisor(dealer, slab, advisor, None) :
                                    available_slabs.append(slab_detail)
                        else:
                            available_slabs.append(slab_detail)
                slab = slab + datetime.timedelta(minutes = timings["slot"])
        return   available_slabs
    
    
    def get_capacity_for_slab(self,slab_time,dealer):
        total_techs = self.get_available_techs_count_for_slab_db(slab_time, dealer)
        
        return total_techs
         
         
    def get_capacity_for_date(self,slab_time,dealer):
        total_techs = self.get_available_techs_for_date(slab_time, dealer)
        
        shop_timings = self.dealership_service.get_dealer_shop_time(slab_time,dealer.id)
        
        capacity_per = 100
        hours = 9
        
        if shop_timings:
            capacity_per = shop_timings["capacity"]
            difference = shop_timings["close_time"] - shop_timings["open_time"]  # difference is of type timedelta
            
            hours = difference.seconds / 60 / 60  # convert seconds into hour
        
       
        total_capacity = (hours * len(total_techs) * 3) * capacity_per/100     
        
        return total_capacity
        
            
    def check_slab_availibity(self,slab_time,dealer,appointment=None):
        """slab_time should be timezone aware time"""
        
        self.setservices()
        capacity_per = 100
        shop_timings = self.dealership_service.get_dealer_shop_time(slab_time,dealer.id)
        if shop_timings:
            capacity_per = shop_timings["capacity"]
        
        if appointment and appointment.advisor :
            if self.check_slab_for_advisor( dealer,slab_time,appointment.advisor)==False:
                return False
            

        
        total_capacity_slab = self.get_capacity_for_slab(slab_time, dealer)
        total_capacity = self.get_capacity_for_date(slab_time,dealer)#new method to get capacity for date
            
#       total_capacity =  round(total_capacity * (capacity_per/100.0))#getting percentage of capacity
        total_appointments_count = 0
        total_appointments_count_slab = 0
        total_appointments_slab = self.appointment_service.get_active_appointment_by_time(slab_time, dealer,None,appointment)
        total_appointments = self.appointment_service.get_active_appointment_by_date(slab_time, dealer,None,appointment)
            
        
        if total_appointments:
            total_appointments_count = len(total_appointments)
        if total_appointments_slab:
            total_appointments_count_slab = len(total_appointments_slab)
        if total_capacity> total_appointments_count:
            print total_capacity_slab
            print total_appointments_count_slab
            if total_capacity_slab > total_appointments_count_slab:
                return True
       
        return False
    
    
    def check_slab_for_advisor(self,dealer,slab_time,advisor,appointment=None):
        self.setservices()
        if self.check_user_availabe_for_slab(slab_time,advisor):
            if self.appointment_service.get_active_appointment_by_time(slab_time,dealer,advisor,appointment):
                return False
            return True
        else: 
            return False
    
    
    def save_tech_count_for_date_range(self,slab_start_date,slab_end_date,dealer):
        """
                slab_start_date : date object
                slab_end_date: date object
                dealer : dealer object
        """
        self.setservices()
        
        for n in range(int ((  slab_end_date - slab_start_date).days)):
            dt = slab_start_date + timedelta(n)
            self.save_tech_count_for_date(dt, dealer)
            
            
    def save_tech_count_for_date(self,slab_date,dealer):
        timings = self.dealership_service.get_dealer_shop_time(slab_date, dealer.id)
        if timings:
            slab = timings["open_time"]     
             
            while slab < timings["close_time"]:       
    #                 tmp_slab_up = slab + datetime.timedelta(minutes = timings["slot"])
    #                 if timings["on"]:
                        self.save_tech_count_for_slab(slab, dealer)
                        slab = slab + datetime.timedelta(minutes = timings["slot"])
              
        
        
    def save_tech_count_for_slab(self,slab_time,dealer):
#         print slab_time
        count = self.get_available_techs_count_for_slab(slab_time, dealer)
        try:
            capacitycount = CapacityCounts.objects.get(time_slab=slab_time,dealer=dealer)
        except Exception,e:
            capacitycount = CapacityCounts()
            capacitycount.time_slab=slab_time
            capacitycount.dealer = dealer
        capacitycount.total_tech = count
        capacitycount.save()
    
    
    def get_available_techs_for_slab(self,slab_time,dealer):
        self.setservices()
        try:
            techs =  self.cuserservice.get_users_for_dealers(dealer.id)
        except Exception,e:   
            techs =  self.cuserservice.get_users_for_dealers(dealer)
        techs_list = []
        if techs:
            for tech in techs:
                if self.check_user_availabe_for_slab(slab_time,tech):
                    techs_list.append(tech)
        return techs_list
    
    def get_available_techs_for_date(self,slab_time,dealer):
        self.setservices()
        try:
            techs =  self.cuserservice.get_users_for_dealers(dealer.id)
        except Exception,e:   
            techs =  self.cuserservice.get_users_for_dealers(dealer)
        techs_list = []
       
        
        if techs:
            for tech in techs:
                user_capacity = self.check_user_available_for_day(slab_time,tech)
                if user_capacity:
                    techs_list.append(tech)
       
        return techs_list
    
    
    
    def get_available_techs_count_for_slab_db(self,slab_time,dealer):
        try:
            capacitycount = CapacityCounts.objects.get(time_slab=slab_time,dealer=dealer)
            return capacitycount.total_tech
        except Exception,e:
            
            return self.get_available_techs_count_for_slab(slab_time,dealer)
        
    def get_available_techs_count_for_slab(self,slab_time,dealer):
        techs = self.get_available_techs_for_slab(slab_time, dealer)
        return len(techs)
    
    
    
    
    
     
           
           
           
    def check_user_availabe_for_slab(self,slab_time,user):
        user_capacity = self.check_user_available_for_day(slab_time,user)
        if user_capacity:
            user_away = self.check_user_away_for_time(slab_time, user)
            if user_away:
                return False
            else:
                return True
        else:
            return False
 
        
    def check_user_away_for_time(self,slab_time,user): 
        filter_aargs = {"start_date__lte" : slab_time.strftime("%Y-%m-%d"),"advisor":user
                      }
        args= ( Q(end_date__gte=slab_time.strftime("%Y-%m-%d")) 
                                                    |Q(end_date=None)
                                                     ,
                                                     )
        day = slab_time.strftime("%A").lower()
        
        
        try:
            restrictions  = AdvisorRestrictions.objects.filter(*args,**filter_aargs)
            restrictions_values = restrictions.values('id',
                                           'monday',
                                           'tuesday',
                                           'wednesday',
                                           'thursday',
                                           'friday',
                                           'saturday',
                                           "start_time","end_time",
                                           )
            for restriction in restrictions_values:
                if  restriction.get(day,False) == True\
                 and slab_time.time() >= restriction["start_time"] and  slab_time.time() <= restriction["end_time"]:
                    return True
            return False
        except Exception,e:
            print e
            return False
            
    
    
    def check_user_available_for_day(self,slab_time,user):
        day = slab_time.strftime("%A").lower()
        user_capacity = False
        try:
            user_capacity = AdvisorCapacity.objects.get(advisor=user)
#             user_capacity_values = user_capacity.values('id',
#                                            'monday',
#                                            'tuesday',
#                                            'wednesday',
#                                            'thursday',
#                                            'friday',
#                                            'saturday',
#                                            )
        except Exception,e:
            print e
        if user_capacity:
            if hasattr(user_capacity,day)  and getattr(user_capacity,day) ==False:
                return False
        return True