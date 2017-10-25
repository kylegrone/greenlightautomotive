import math

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.views.decorators.csrf import csrf_protect

from customer.forms import GuestccountForm as CustomerGuestAccountForm, CustomerVehichleForm
from customer.services.userservices import CUserService
from dealership import conf
from dealership.decorators import *
from dealership.decorators import dealer_group_check
from dealership.factories import DealerShipServicesFactory
from dealership.forms import *
from dealership.services.appointmentservices import AppointmentService
from dealership.services.breadcrumb import BreadCrumb
from dealership.services.repairservices import RepairService
from dealership.services.userservices import UserService
from dealership.services.vehicleservices import VehicleService
from dealership.services.wayawayservices import WayAwayService
import json as mainjson


@dealership_access_check
def appointment(request):
    searchform = SearchCustomerForm()
    custform = CustomerGuestAccountForm()
    vehicleform = CustomerVehichleForm() 
    apptform = GuestAppointmentForm() 
    guestform =  GuestAccountForm() 
    aptservice = AppointmentService() 
    dealer_factory = DealerShipServicesFactory() 
    dealer_service = dealer_factory.get_instance("dealership")
    vehicle_service = dealer_factory.get_instance("vehicle")
    dealer = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    vehichles = vehicle_service.get_vehichles_dealer(dealer)
    vehicles = list(vehichles)   
    breadcrumb = BreadCrumb()
    breadcrumb = breadcrumb.create_breadcrumb(["appointment"])
    status = aptservice.get_appointments_status()
    wayaway = aptservice.get_wayaway()
    advisors = aptservice.get_appointments_advisor(request.session["dealer_id"])
    wallboard = aptservice.get_appointments_wallboard_data(request.session["dealer_id"])
    template = 'appointment/index.html'
    qstring = {}
    for key, value in request.GET.iteritems():
        qstring[key] = value
    
    dealer_service = dealer_factory.get_instance("dealership")
    favorites = dealer_service.get_dealer_favorites(request.session["dealer_id"])
    
    config = {"username":request.user,
              "dealer_code":request.session["dealer_code"],
              "dealer_name":request.session["dealer_name"],
              "dealer_id":request.session["dealer_id"],
              "group":request.session["group"],
              "tab":"appointment",
              "CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
              "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET}
    
    return render(request, template,  {'config':config,
                                       "favorites":favorites,
                                       'breadcrumb':breadcrumb, 
                                       'wallboard':wallboard, 
                                       'searchform':searchform, 
                                       'qstring':qstring,
                                       'searchform':searchform,  
                                       'custform':custform,
                                       'guestform':guestform,
                                       'vehicleform':vehicleform,
                                       'apptform':apptform,
                                       'vehicles':mainjson.dumps(vehicles),               
                                       'status':status['data'],
                                       'wayaway':wayaway['data'],
                                       'advisors':advisors,
                                       'qstring':qstring})

# @dealership_services_access_check
def appointment_time_ajax_view(request):

    template = 'appointment/time.html'
    grid_data = {}
    if request.method == 'POST': 
        aptservice = AppointmentService()
        grid_data = aptservice.get_weekly_time_grid(request.POST.get('appt_id'),
                                                    request.POST.get('date'),
                                                    request.session["dealer_id"])        
    return render(request, template, {'grid_data':grid_data})

# @dealership_services_access_check
def appointment_wayaway_ajax_view(request):
    dealer_factory = DealerShipServicesFactory()
    appointment_service = dealer_factory.get_instance("appointment")
    dealership_service = dealer_factory.get_instance("dealership")
    template = 'appointment/wayaway.html'
    wayaway = WayAwayService()
    cuser = CUserService()
   
    selected_wayaway = None
    appointment = None
    user_id = None
    profile = None
    dealer = None
    if request.method == 'POST':
#         selected_wayaway = wayaway.get_apt_wayaway() 
        if request.POST.get("user_id")!=0:
            profile = cuser.get_user_profile(request.POST.get("user_id"))
        if request.POST.get("dealer_code")!=0:
            dealer = dealership_service.get_dealer_by(request.POST.get("dealer_code"))
        appointment = appointment_service.get_valid_appointment(request.POST.get('appt_id'))
        
    wyay = wayaway.get_all_wayaway(dealer)
    states = wayaway.get_all_states()   
    return render(request, template, {'appointment':appointment, 
                                      'wayaway':wyay , 'states':states,"profile":profile})

# @dealership_services_access_check
def appointment_wayaway_save_ajax(request):
    wayaway = WayAwayService()
    cuser = CUserService()
    if request.method == 'POST': 
       
        if request.POST.get('appt_id'):
            wa = wayaway.update_wayaway(request.POST.get('appt_id'),
                                    request.POST.get('wayaway'),
                                    driver_liscens_number=request.POST.get('dl'),
                                    insurance_company_name=request.POST.get('company'),
                                    insurance_card_number=request.POST.get('card'),
                                    state_id= request.POST.get('state'),
                                    reserve = request.POST.get("reserve",0)
                                    )
#             try:
#                 user_id = request.POST.get('user_id')
#                 user = User.objects.get(id = user_id)
#             except Exception,e:
#                 print e
#                 user = None
#             IP = cuser.get_user_driver_insurance(user)
#             IP.driver_liscens_number = request.POST.get('DL')
#             IP.insurance_company_name = request.POST.get('company')
#             IP.insurance_card_number = request.POST.get('card')
#             IP.state_id = request.POST.get('state')
#             IP.save() 
        return JsonResponse({"appt_id":request.POST.get('appt_id')})
    return JsonResponse({"appt_id":0})


# @dealership_services_access_check
def appointment_repair_ajax_view(request):
    template = 'appointment/service.html'
    repairservice = RepairService()
    appointment_id = 0
    page_limit = 4
    if request.method == 'GET' and 'appt_id' in request.GET:
        appointment_id = request.GET['appt_id']
    if request.method == 'POST' and 'appt_id' in request.POST:
        appointment_id = request.POST.get('appt_id')
    services = repairservice.get_all_service_repair_dealer_appt('s', request.session["dealer_id"], appointment_id)
    if len(services) % page_limit > 0:
        services_pages = range(0, len(services)/page_limit+1)
    else:
        services_pages = range(0, len(services)/page_limit)
        
    print "line 131" 
    print services
    #services = [services[i:i+12] for i  in range(0, len(services), 12)]
    repairs = repairservice.get_all_service_repair_dealer_appt('r', request.session["dealer_id"], appointment_id)
    
    if len(repairs) % page_limit > 0:
        repairs_pages = range(0, len(repairs)/page_limit+1)
    else:
        repairs_pages = range(0, len(repairs)/page_limit)
    #repairs = [repairs[i:i+12] for i  in range(0, len(repairs), 12)]
    data = []
    if request.method == 'POST': 
        data = repairservice.create_update_appointment_services(request.POST.get('appt_id') ,request.POST.getlist('rservice[]') )        
    return render(request, template, {'services':services,'services_pages':services_pages,'repairs':repairs , 'repairs_pages':repairs_pages, 'sr_ids' : data})

# @dealership_services_access_check
def appointment_customer_ajax_view(request):
    template = 'appointment/customer.html'
    customer = {}
    vehicles = {}
    dealer_factory = DealerShipServicesFactory()  
    dealer = Dealer.objects.get(id = request.session.get("dealer_id"))
    if request.method == 'POST': 
        userservice = UserService()
        vehicleservice = VehicleService()
        user_id = request.POST.get('user_id');
        try:
            user_cus = UserProfile.objects.get(id=user_id)
            cusform = CustomerGuestAccountForm(instance =user_cus)
        except:
            cusform = None
        customer = userservice.get_customer_detail(user_id) 
        if request.POST.get('vehicle_id'):
            template = 'appointment/customer_vehicle_selected.html'
            vehicles = vehicleservice.get_customer_vehicles(user_id, dealer, request.POST.get('vehicle_id'), request.POST.get('appointment_id'))
        else:
            vehicles = vehicleservice.get_customer_vehicles(user_id, dealer)
        
        try:
            customer_advisor = CustomerAdvisor.objects.get(dealer_id=dealer.id,customer_id=user_cus)
        except:
            
            customer_advisor = None
        
    return render(request, template, {'customer':customer, 
                                      'vehicles':vehicles, 
                                      'cusform' :cusform,
                                      "customeradvisor":customer_advisor
                                      })  

# @dealership_services_access_check
def customer_delete_vehicle_ajax_view(request):
    context = {}
    if request.method == 'POST': 
        vehicleservice = VehicleService()
        context["success"] = vehicleservice.delete_customer_vehicle(request.POST.get('cust_veh_id'))    
    return JsonResponse(context)

# @dealership_services_access_check
def appointment_create_update(request):
    context = {}
    if request.method == 'POST': 
        data = {}
        for key, value in request.POST.iteritems():
            if key == "start_time":
                #value = datetime.datetime.strptime(value, '%b. %d, %Y, %I:%M %p')
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')
                value = timezone.make_aware(value)
               
            data[key] = value
        aptservice = AppointmentService()
        context = aptservice.create_update_appointment(data)  
    return JsonResponse(context)

# @dealership_services_access_check
def appointment_account_info_ajax_view(request):
    cuser = CUserService()
    UI=None
    if request.method == 'POST':
        if request.POST.get('user_id'):
            user_id = request.POST.get('user_id')
            user = UserProfile.objects.get(id = user_id)
            UI = cuser.get_user_driver_insurance(user)
    if UI and UI.insurance_company_name!=None and UI.insurance_card_number!=None and UI.driver_liscens_number!=None:
        return JsonResponse({"success":True,'company': UI.insurance_company_name , 
                             'card': UI.insurance_card_number , 'state': UI.state_id ,
                              'DL' : UI.driver_liscens_number})  
    else:
        return  JsonResponse({"success":False,'company': "" , 
                             'card': "" , 'state': "" ,
                              'DL' : ""}) 

# @dealership_services_access_check         
def appointment_book_ajax_view(request):
    appointment = {}
    template = 'appointment/partials/confirmation_modal_content.html'
    dealer_factory = DealerShipServicesFactory()
    aptservice = dealer_factory.get_instance("appointment")
    if request.method == 'POST': 
        aptservice = AppointmentService()
        #try:
        
        data = {}
        for key, value in request.POST.iteritems():
            if key == "start_time":
                #value = datetime.datetime.strptime(value, '%b. %d, %Y, %I:%M %p')
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')
                value = timezone.make_aware(value)
            data[key] = value
        aptservice = AppointmentService()
        context = aptservice.create_update_appointment(data) 
        
        
        aptservice.book_appointment_with_id(request.POST.get('id'),
                                                  request.session["dealer_id"]) 
        appointment = aptservice.get_appointment_by_id(request.POST.get('id'));
        print  appointment
        #except Exception, ex:
            #pass
        
    return render(request, template, appointment) 


def appointment_remove_service(request):
    status = False
    dealer_factory = DealerShipServicesFactory()
    repair_service = dealer_factory.get_instance("repair")
    if request.method == 'POST': 
        status = repair_service.remove_service(request.POST.get('id'))
        return JsonResponse({"status":status})
    return JsonResponse({"status":status})