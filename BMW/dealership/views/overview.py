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
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import resolve

from dealership import conf
from dealership.decorators import dealer_group_check
from dealership.forms import *
from dealership.decorators import *

#from dealership.services.appointmentservices import AppointmentService
#from dealership.services.vehicleservices import VehicleService

from dealership.services.breadcrumb import BreadCrumb
from customer.forms import CreditDebitForm, CustomerVehichleForm, GuestccountForm as CustomerGuestAccountForm
from customer.factories import CustomerServicesFactory
from dealership.factories import DealerShipServicesFactory

import json as mainjson

#@user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
@dealership_access_check
def overview(request):
    dealer_factory = DealerShipServicesFactory()
    searchform = SearchCustomerForm()
    custform = CustomerGuestAccountForm()
    vehicleform = CustomerVehichleForm() 
    apptform = GuestAppointmentForm() 
    guestform =  GuestAccountForm() 
    vehicle_service = dealer_factory.get_instance("vehicle")
    dealer =Dealer.objects.get(id=request.session["dealer_id"])
    vehichles = vehicle_service.get_vehichles_dealer(dealer)
    vehicles = list(vehichles) 
    aptservice = dealer_factory.get_instance("appointment")
    dealer_service = dealer_factory.get_instance("dealership")
    capacity_service = dealer_factory.get_instance("capacity")
    
    breadcrumb = BreadCrumb()
    breadcrumb = breadcrumb.create_breadcrumb(["overview"])
    wallboard = aptservice.get_appointments_wallboard_data(request.session["dealer_id"])
    status = aptservice.get_appointments_status()
    wayaway = aptservice.get_wayaway()
    timings = dealer_service.get_dealer_shop_time( timezone.now() , request.session["dealer_id"])
    capacity   = capacity_service.get_capacity_for_date(timezone.now(),dealer)
    today_appts = aptservice.get_active_appointment_by_date(timezone.now(),dealer)
    print today_appts
    total_aptts_total = 0
    if today_appts:
        total_aptts_total =len(today_appts)
    template = 'overview/index.html'
    qstring = {}
    try:
        qstring = {'search':request.GET["search"], 'criteria':request.GET["criteria"]}
    except:
        pass
    
    favorites = dealer_service.get_dealer_favorites(request.session["dealer_id"])
  
    config = {"username":request.user,
                "dealer_code":request.session["dealer_code"],
                
                "dealer_name":request.session["dealer_name"],
                "dealer_id":request.session["dealer_id"],                
                "group":request.session["group"],              
                "tab":"overview",
                "CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
                "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET}
    
    return render(request, template, {"config":config,  
                                      "favorites":favorites,                                    
                                      "timings":timings,
                                      'breadcrumb':breadcrumb,
                                      'wallboard':wallboard,
                                      'searchform':searchform,
                                      'custform':custform,
                                      'guestform':guestform,
                                      'vehicleform':vehicleform,
                                      'apptform':apptform,
                                      'vehicles':mainjson.dumps(vehicles),
                                      'qstring':qstring,
                                      'status':status['data'],
                                      'wayaway':wayaway['data'],
                                      "code":request.session["dealer_code"],
                                      "totalcapacity":capacity,"appts_total":total_aptts_total
                                      })


#@user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
@dealership_access_check
def ov_time_daily(request):
    dealer_factory = DealerShipServicesFactory()
    template = 'overview/time_daily.html'
    if request.method == 'GET' and 'template' in request.GET:
        template = request.GET['template']
    if request.method == 'POST' and 'template' in request.POST:
        template = request.POST.get('template')
    dealer_service = dealer_factory.get_instance("dealership")
    breadcrumb = BreadCrumb()
    if request.method == 'GET' and 'q' in request.GET:
        filter = "_%s" % (request.GET['q'])
    date = datetime.datetime.now()
    if request.method == 'GET' and 'date' in request.GET:
        date = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d %H:%M') 
    timings = dealer_service.get_dealer_shop_time(date, request.session["dealer_id"])
    breadcrumb = breadcrumb.create_breadcrumb(["overview", "ov_time_daily%s" % (filter)])
    return render(request, template, {'breadcrumb':breadcrumb, 'timings':timings})

#@user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
@dealership_access_check
def ov_time_weekly(request):
    dealer_factory = DealerShipServicesFactory()
    template = 'overview/time_weekly.html'
    dealer_service = dealer_factory.get_instance("dealership")
    breadcrumb = BreadCrumb()
    if request.method == 'GET' and 'q' in request.GET:
        filter = "_%s" % (request.GET['q'])
    date = datetime.datetime.now()
    if request.method == 'GET' and 'date' in request.GET:
        date = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d %H:%M') 
    timings = dealer_service.get_dealer_shop_time(date, request.session["dealer_id"])
    breadcrumb = breadcrumb.create_breadcrumb(["overview", "ov_time_weekly%s" % (filter)])
    return render(request, template, {'breadcrumb':breadcrumb, 'timings':timings})

#@user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
@dealership_access_check
def wallboard_ajax_view(request):
    dealer_factory = DealerShipServicesFactory()
    aptservice = dealer_factory.get_instance("appointment")
    
    wallboard = aptservice.get_appointments_wallboard_data(request.session["dealer_id"], request.POST.get('date'))
    
    template = 'dealership/app/wallboard.html'
    return render(request, template, {'wallboard':wallboard})

#@user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
@dealership_access_check
def searchcustomer_ajax_view(request):
    template = 'overview/searchcustomer.html'
    searchform = SearchCustomerForm()    
    return render(request, template, {'searchform': searchform})

#@user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
@dealership_access_check
def dailyapt_ajax_view(request):
    template = 'overview/time_daily_slab.html'
    if request.method == 'GET' and 'template' in request.GET:
        template = request.GET['template']
    if request.method == 'POST' and 'template' in request.POST:
        template = request.POST.get('template')
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appoiontments_by_time(request.POST.get('datetime'),
                                                       request.session["dealer_id"],
                                                       request.POST.get('advisor_id'))      
           
    return render(request, template, context)

@dealership_access_check
def advisor_daily_slab_ajax_view(request):
    template = 'overview/time_daily_slab.html'
    context = {}
    print "new function "
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_by_advisor(request.POST.get('date'),
                                                         request.session["dealer_id"],
                                                         request.POST.get('id'))      
        print context   
    return render(request, template, context)

@dealership_access_check
def status_daily_slab_ajax_view(request):
    template = 'overview/time_daily_slab.html'
    context = {}
    print "new function "
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_by_status(request.POST.get('date'),
                                                        request.session["dealer_id"],
                                                        request.POST.get('id'))      
        print context   
    return render(request, template, context)

@dealership_access_check
def time_daily_search_ajax_view(request):
    #template = 'overview/time_daily_multi_slab.html'
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_by_time_criteria(request.POST.get('date'),
                                                               request.session["dealer_id"],
                                                               request.POST.get('search'),
                                                               request.POST.get('criteria'))       
    return JsonResponse(context)
    #return render(request, template, context)
    
@dealership_access_check
def time_daily_search_appt_ajax_view(request):
    template = 'overview/time_daily_multi_slab.html'
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_by_time_id(request.POST.get('appt_id'), request.session["dealer_id"])        
    return render(request, template, context)     

@dealership_access_check
def time_weekly_slab_ajax_view(request):
    template = 'overview/time_weekly_slab.html'
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appoiontments_by_time(request.POST.get('datetime'),
                                                       request.session["dealer_id"])      
        context["id"] = request.POST.get('id')
    return render(request, template, context)

@dealership_access_check
def advisor_weekly_slab_ajax_view(request):
    template = 'overview/time_weekly_slab.html'
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_by_advisor(request.POST.get('date'),
                                                         request.session["dealer_id"],
                                                         request.POST.get('id'))      
        context["id"] = "%s_%s" % (request.POST.get('date').replace("-", "_"),request.POST.get('id'))
    return render(request, template, context)

@dealership_access_check
def status_weekly_slab_ajax_view(request):
    template = 'overview/time_weekly_slab.html'
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_by_status(request.POST.get('date'),
                                                        request.session["dealer_id"],
                                                        request.POST.get('id'))      
        context["id"] = "%s_%s" % (request.POST.get('date').replace("-", "_"),request.POST.get('id'))
    return render(request, template, context)

@dealership_access_check
def appointment_row_ajax_view(request):
    template = 'overview/time_daily_row.html'
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = {'row':aptservice.get_appointment_by_id(request.POST.get('id'))}    
        print context
    return render(request, template, context)

@dealership_access_check
def time_weekly_day_ajax_view(request):
    template = 'overview/time_weekly_day.html'
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_day(request.POST.get('date'),
                                                  request.session["dealer_id"],
                                                  request.POST.get('type'))      
        context['id'] = request.POST.get('id')    
    return render(request, template, context)

@dealership_access_check
def appointment_detail_ajax_view(request):
    template = 'overview/detail.html'
    context = {}
    customer_factory = CustomerServicesFactory()
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        vehicleservice = dealer_factory.get_instance("vehicle")
        service = customer_factory.get_instance("user")
        account_service =  customer_factory.get_instance("account")
        userprofile =service.get_user_profile(request.POST.get('customer_id'))
        context = aptservice.get_appointment_by_id(request.POST.get('appointment_id'));
        print context['appointment'].checkin_time,"$$$$$$$$$$"
        #get credit card form        
        cc_profile = service.get_cc_profile(userprofile)
        cc_initial = account_service.get_initial_cc_form(request.POST.get('customer_id'),cc_profile,userprofile)
        cc_form = CreditDebitForm(instance=cc_profile,initial=cc_initial)        
        context['cc_form'] = cc_form 
        #get vechicle information form
        vehicle_instance = vehicleservice.get_customer_vehicle(request.POST.get('vehicle_id'))
        vehicle_form = CustomerVehichleForm(instance=vehicle_instance) 
        context['vehicle_form'] = vehicle_form
        #insurence form
        insurance_profile = service.get_user_driver_insurance(userprofile)
        driver_initial  =account_service.get_initial_driver_form(request.POST.get('customer_id'), insurance_profile,userprofile)
        ins_form = CustomerInsuranceForm(instance=insurance_profile,initial=driver_initial)
        context['ins_form'] = ins_form   
        
        if request.POST.get('checkin'): 
            context['checkin'] = 'true'
        else:
            context['checkin'] = 'false'   
        
        
            
    return render(request, template, context)

@dealership_access_check
def appointment_update_creditcard(request):
    customer_factory = CustomerServicesFactory()
    service = customer_factory.get_instance("user")
    account_service =  customer_factory.get_instance("account")
    if request.method == 'POST':         
        userprofile =service.get_user_profile(request.POST.get('user'))
        cc_profile = service.get_cc_profile(userprofile)
        cc_form = CreditDebitForm(request.POST,instance = cc_profile)
        if cc_form.is_valid():
            resp = account_service.save_cc_form(cc_profile,cc_form)
            if resp == True:
                return JsonResponse({"status":"success", "message":"Credit Card Information Updated Successfully"})
            else:
                return JsonResponse({"status":"error", "message":"Credit Card Information Failed to Update"})
        else:
            return JsonResponse({"status":"error", "message":"Credit Card Data is not Valid"})
            #return JsonResponse({"status":"error", "errors":cc_form.errors})
    return JsonResponse({"status":"error"})

@dealership_access_check        
def appointment_update_vehicle(request):   
    dealer_factory = DealerShipServicesFactory()
    vehicleservice = dealer_factory.get_instance("vehicle") 
    if request.method == 'POST':
        vehicle_instance = vehicleservice.get_customer_vehicle(request.POST.get('id'))
        vehicle_form = CustomerVehichleForm(request.POST, instance = vehicle_instance)
        if vehicle_form.is_valid():
            result = vehicle_form.save()
            #return JsonResponse({"status":"success", "id":result.pk})
            return JsonResponse({"status":"success", "message":"Vehicle Information Updated Successfully"})            
        else:
            return JsonResponse({"status":"error", "message":"Vehicle Data is not Valid"})
    return JsonResponse({"status":"error"})
                    
@dealership_access_check
def appointment_update_insurance(request):
    customer_factory = CustomerServicesFactory()
    service = customer_factory.get_instance("user")
    account_service =  customer_factory.get_instance("account")
    if request.method == 'POST':
        userprofile =service.get_user_profile(request.POST.get('user'))
        insurance_profile = service.get_user_driver_insurance(userprofile)
        driver_initial  =account_service.get_initial_driver_form(request.POST.get('customer_id'), insurance_profile,userprofile)
        driver_form = CustomerInsuranceForm(request.POST,instance = insurance_profile, initial=driver_initial)
        if driver_form.is_valid():
            resp = driver_form.save()
            #result = account_service.save_driver_form(insurance_profile,driver_form)
            return JsonResponse({"status":"success", "message":"Insurance Information Updated Successfully"})
   
        else:
            return JsonResponse({"status":"error", "message":"Insurance Data is not Valid"})
    return JsonResponse({"status":"error"})            

@dealership_access_check
def advisor_ajax_view(request):
    #template = 'overview/daily_slab.html'
    context = {}
    #print "old function "
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        if request.POST.get('datetime'):
            context = aptservice.get_appointments_advisor(request.session["dealer_id"],
                                                          request.POST.get('datetime'))   
        else:  
            context = aptservice.get_appointments_advisor(request.session["dealer_id"])
        #context['id'] = request.POST.get('id')    
    #return render(request, template, context)
    return JsonResponse({'data':context})

@dealership_access_check
def status_ajax_view(request):
    """
    status_ajax_view
    *get list of all the status from appointmentstatus table along with calculated capacity
    """
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_appointments_status()     
    return JsonResponse(context)

@dealership_access_check
def wayaway_ajax_view(request):
    """
    wayaway_ajax_view
    *get list of all the wayaway options from along with calculated capacity
    """
    context = {}
    if request.method == 'POST': 
        dealer_factory = DealerShipServicesFactory()
        aptservice = dealer_factory.get_instance("appointment")
        context = aptservice.get_wayaway()     
    return JsonResponse(context)
