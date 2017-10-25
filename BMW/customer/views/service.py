from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.http.response import JsonResponse, HttpResponse

from customer.decorators.decorators import dealership_required, \
    appointment_required
from customer.factories import CustomerServicesFactory
from customer.services.userservices import CUserService
from dealership.factories import DealerShipServicesFactory
from dealership.services.appointmentservices import AppointmentService
from dealership.services.dealershipservice import DealerShipService
from dealership.services.repairservices import RepairService
from dealership.services.twilio_service import TwillioService
import json as mainjson
from dealership.models import CustomerAdvisor


def send_activation_code(request):
    if request.GET.get("phone_number") :
        phone_number = request.GET.get("phone_number")
        twilios  = TwillioService()
        body = "123"
        twilios.send_message(body,phone_number,twilios.default_number)
        return JsonResponse({"success":True,"text":body},safe=False) 
    else:
        return JsonResponse({"success":False,"text":""},safe=False) 
    
  
def save_customer_number(request):
    if request.GET.get("phone_number"):
        customer_factory = CustomerServicesFactory()
        user_service = customer_factory.get_instance("user")
        profile = user_service.get_userprofile(request.user)
        phone_number = request.GET.get("phone_number")
        carrier_choices = request.GET.get("carrier")
        user_service.save_active_phone(profile,phone_number,carrier_choice=carrier_choices)
        return JsonResponse({"success":True},safe=False) 
    else:
        return JsonResponse({"success":False},safe=False) 

@dealership_required
def save_advisor(request,dealer_code):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    resp = True
    user=None
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    rtype=  request.GET.get("type","appointment")
    if rtype == "appointment":
#         if request.GET.get("advisor_id"):
            try:
                appointment_id = request.GET.get("appointment_id")
                     
                service = AppointmentService()
                appointment = service.get_appointment(appointment_id)
                advisor_id = request.GET.get("advisor_id",appointment.advisor_id)
                save_advisor = service.save_advisor(appointment,advisor_id)
                cservice = customer_factory.get_instance("user")#CUserService()
                if save_advisor: 
                    resp = True
                print appointment.customer.id
                print dealership.id
                print advisor_id
                save = cservice.save_my_advisor(appointment.customer.id,dealership.id,advisor_id)
                if save==False:
                    resp= False
            except Exception,e:
                print e
    elif rtype == "user":
        if request.GET.get("advisor_id"):
            try:
                profile_id = request.GET.get("profile_id")
                advisor_id =request.GET.get("advisor_id")
                service = customer_factory.get_instance("user")#CUserService()
                save = service.save_my_advisor(profile_id,dealership.id,advisor_id)
                if save:
                    resp = True
                appointment_id = request.GET.get("appointment_id")
                    
            except Exception,e:
                print e
   
    else:
        print "error"
   
     
    return JsonResponse({"success":resp},safe=False) 



@dealership_required
def get_all_advisor(request,dealer_code):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    service_layer = customer_factory.get_instance("user")#CUserService()
    media_url = settings.MEDIA_URL
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    selected_advisor_id = None
    appointment =None
    rtype=  request.GET.get("type","appointment")
    profile_id = request.GET.get("profile_id")
    """when saving for appointment"""
    if rtype == "appointment":
        appointment_id = request.GET.get("appointment_id")
        service = dealer_factory.get_instance("appointment")#AppointmentService()
        appointment = service.get_appointment(appointment_id)        
        if appointment and appointment.advisor:
            selected_advisor_id = appointment.advisor.id    
        if selected_advisor_id ==None and appointment:
            try:
                customer_advisor =CustomerAdvisor.objects.get(customer_id=appointment.customer.id)
                selected_advisor_id=customer_advisor.advisor.id
            except Exception,e:
                print e
                customer_advisor = None
  
    elif rtype =="user":
        """when saving for user""" 
        if profile_id:
            profile = service_layer.get_user_profile(profile_id)
            myadvisor = service_layer.get_my_advisor(profile_id,dealership.id)
            if myadvisor:
                selected_advisor_id = myadvisor.id 
            
    all_advisors = service_layer.get_all_available_advisor_for(dealer_code,appointment)
    
#     all_advisors = all_advisors.values("id","first_name","last_name","userprofile__avatar")
   
    resp =    {"advisors":list(all_advisors),
               "selected_advisor":selected_advisor_id,
               "mainurl":media_url
               }
    
    return JsonResponse(resp,safe=False) 




@dealership_required
def get_all_services(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    search_text = None
    service_layer = dealer_factory.get_instance("repair")#RepairService()
    selected_services = []
    media_url = settings.MEDIA_URL
    if request.GET.get("appointment_id") !=None:
        appointment_id = request.GET.get("appointment_id")
        stype = request.GET.get("type")
        selected_services = service_layer.get_service_for(appointment_id,stype)
        if selected_services:
            selected_services = selected_services.values("id","note","service__id")
    if request.GET.get("search_text")!=None:
        search_text =   request.GET.get("search_text")
      
    if request.GET.get("type")=="r" or request.POST.get("type")=="r":
        all_services = service_layer.get_all_repairs_for(dealer_code,search_text=search_text)
    else:
        all_services = service_layer.get_all_services_for(dealer_code,search_text=search_text)
    
    all_services = all_services.values("id","dms_opcode","duration","image","name","price","price_unit","type","description")
   
    
   
    resp =    {"services":list(all_services),
               "selected_services_id":list(selected_services),
               "mainurl":media_url
               }
    
    return JsonResponse(resp,safe=False) 


  
@dealership_required      
def save_all_services(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    service_layer = dealer_factory.get_instance("repair")#RepairService()
    success = False
    
    stype = request.GET.get("type")
    if request.GET.get("appointment_id") !=None and request.GET.get("services") !=None :
        appt_id= request.GET.get("appointment_id")
        services = mainjson.loads( request.GET.get("services"))
        service_layer.create_update_delete_appointment_services(appt_id,services,stype)
        success = True
    return JsonResponse({"success":success})
        