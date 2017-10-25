'''
Created on 24-Nov-2015

@author: Shoaib Anwar
'''
from dealership.models import *
import datetime
import time
import math

from dealership import conf
from django.contrib.auth.models import User
from dealership.models import UserProfile
#from dealership.services.userservices import UserService
from dealership.services.vehicleservices import VehicleService
from django.db.models import Q
from django.db.models import Count

from django.core import serializers
from django.utils import timezone

class CustomerService():   
    
    def setservices(self):
        from dealership.factories import DealerShipServicesFactory
        self.dealer_service_factory = DealerShipServicesFactory()      
        self.vehicle_service = self.dealer_service_factory.get_instance("vehicle")
        self.appointment_service = self.dealer_service_factory.get_instance("appointment")
        self.customer_service = self
         
    def get_customer_list(self, dealer, cust_id, page = 1, limit = 10):
        self.setservices()
        start = (page*limit - limit)
        end = page*limit
        if cust_id == 0:
            count = UserProfile.objects.filter(Q(user__groups__name__in = ['Customer']) | Q(user__isnull = True) ).count()
            customers = UserProfile.objects.filter(Q(user__groups__name__in = ['Customer']) | Q(user__isnull = True)).order_by('first_name')[start:end]
        else:
            cust_id = cust_id.split(",")
            count = UserProfile.objects.filter(id__in = cust_id).count()
            customers = UserProfile.objects.filter(id__in = cust_id).order_by('first_name')[start:end]
        data = []
        for cust in customers:  
            appt = "None"          
            vehicles = self.vehicle_service.get_customer_vehicles(cust.id, dealer)
            if vehicles is None:
                vehicles = []
           
            appointments = self.appointment_service.get_customer_secheduled_appointments_for_dealer(cust.id, dealer.id)
            if appointments:
                appt = appointments[0].start_time.strftime('%A %b %d, %I:%M %p')            
                    
            advisor_name = "NO ADVISOR"
            try:
                advisor_name = "%s %s" % (cust.myadvisors.advisor.first_name.upper(), cust.myadvisors.advisor.last_name.upper())
            except Exception, ex:
                pass
            
            profile = "Partial"    
            try:
                user_id = cust.user.id
                profile = "Complete"
            except Exception, ex:
                pass
            
             
                
                
            data.append({'id':cust.id,
                         'name':"%s %s" % (cust.first_name.upper(), cust.last_name.upper()),
                         'vehicle':{'count':len(vehicles), 'list':vehicles},
                         'advisor':advisor_name,
                         'appt':appt,
                         'profile':profile})   
        return {"total":count, "page": page, "limit": limit, "data":data}
    