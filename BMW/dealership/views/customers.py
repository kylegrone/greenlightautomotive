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
from customer.forms import GuestccountForm as CustomerGuestAccountForm, CustomerVehichleForm
from dealership.services.customerservices import CustomerService
from dealership.services.breadcrumb import BreadCrumb
from dealership.factories import DealerShipServicesFactory
from customer.factories import CustomerServicesFactory

import json as mainjson

@dealership_access_check
def customers(request):    
    searchform = SearchCustomerForm()
    custform = CustomerGuestAccountForm()
    vehicleform = CustomerVehichleForm() 
    apptform = GuestAppointmentForm() 
    guestform =  GuestAccountForm() 
    custservice = CustomerService()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    vehicle_service = dealer_factory.get_instance("vehicle")
    dealer = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    vehichles = vehicle_service.get_vehichles_dealer(dealer)
#     vehichles = vehicle_service.get_vehichles()
    vehicles = list(vehichles)
    breadcrumb = BreadCrumb()
    breadcrumb = breadcrumb.create_breadcrumb(["customers"]) 
    
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    dealer = dealer_service.get_dealer_by(request.session.get("dealer_code"))    
    
    
    
    template = 'customers/index.html'
    qobject = {}
    for key, value in request.GET.iteritems():
        qobject[key] = value
   
    page = 1
    limit = 20
    if "page" in qobject:
        page = qobject['page']
        del qobject['page']
    
    qstring = ""   
    for key in qobject:
        qstring += "%s=%s&" %(key, qobject[key])
        
    cust_id = 0
    if request.GET.get('customer_id'):
        cust_id = request.GET.get('customer_id')
          
    customer_list = custservice.get_customer_list(dealer, cust_id, int(page), limit)
 
    
    favorites = dealer_service.get_dealer_favorites(request.session["dealer_id"])
    
    config = {"username":request.user,
              "dealer_code":request.session["dealer_code"],
              "dealer_name":request.session["dealer_name"],
              "dealer_id":request.session["dealer_id"],
              "group":request.session["group"],
              "tab":"customers",
              "CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
              "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET}
    
    return render(request, template, {'config':config,
                                      "favorites":favorites,
                                      'breadcrumb':breadcrumb,
                                      'searchform':searchform,
                                      'custform':custform,
                                      'guestform':guestform,
                                      'vehicleform':vehicleform,
                                      'apptform':apptform,
                                      'vehicles':mainjson.dumps(vehicles),
                                      'list':customer_list,
                                      'qstring':qstring})

@dealership_access_check    
def save_customer_ajax(request):
    dealer_factory = DealerShipServicesFactory()
    user_service = dealer_factory.get_instance("user")
    if request.method == 'POST': 
        guestform = CustomerGuestAccountForm(request.POST)
        if guestform.is_valid():
            customer = guestform.save()
            if request.POST.get('send_link') == "on":                
                user_service.send_registration_link(request, customer.pk)
            return JsonResponse({"status":"success", "id":customer.pk})
        elif guestform.errors:
            return JsonResponse({"status":"error", "errors":guestform.errors})          
    return JsonResponse({"id":0})  

@dealership_access_check
def save_vehicle_ajax(request):
    if request.method == 'POST': 
        vehicleform = CustomerVehichleForm(request.POST)
        if vehicleform.is_valid():
            vehicle = vehicleform.save()
            return JsonResponse({"status":"success", "id":vehicle.pk})
        elif vehicleform.errors:
            return JsonResponse({"status":"error", "errors":vehicleform.errors})          
    return JsonResponse({"id":0})  

@dealership_access_check
def save_appointment_ajax(request):
    if request.method == 'POST': 
        apptform = GuestAppointmentForm(request.POST)
        if apptform.is_valid():
            appointment = apptform.save()
            return JsonResponse({"status":"success", "id":appointment.pk})
        elif apptform.errors:
            return JsonResponse({"status":"error", "errors":apptform.errors})          
    return JsonResponse({"id":0})  

@dealership_access_check
def save_guest_reminder_ajax(request):
    dealer_factory = DealerShipServicesFactory()
    notification_service = dealer_factory.get_instance("notification")
    user_service = dealer_factory.get_instance("user")
    if request.method == 'POST':
        method = {'email':0, 'text':0, 'phone':0}
        method[request.POST.get('method_of_reminder')] = 1
        profile = user_service.get_profile(request.POST.get('customer'))
        reminder = notification_service.create_reminder_setting_for(1, profile)
        notification_service.save_reminder_settings(reminder.id, method['email'],method['text'],method['phone'])
        return JsonResponse({"id":1}) 
    return JsonResponse({"id":0})



@dealership_access_check
def appointment_history(request,customer_id,vehicle_id):
    template = 'customers/apphistory.html'
    appointments = Appointment.objects.filter(customer_id = customer_id , vehicle_id = vehicle_id)
    try:
        customer_vehicle = CustomerVehicle.objects.get(id = vehicle_id)
    except:
        customer_vehicle= None
    return render(request,template,{'apphistory':appointments , 'cv':customer_vehicle})


@dealership_access_check
def edit_customer(request):
    if request.POST:
        customer_factory = CustomerServicesFactory()
        uservice = customer_factory.get_instance("user")
        phone_number = request.POST.get("phone_number_1")
        email = request.POST.get("email_1")
        id = request.POST.get("id")
        profile = uservice.get_user_profile_by_phone(phone_number)
        if profile ==None or profile.id == id:
            profile = uservice.get_user_profile_by_email(email)
        if profile ==None or profile.id == id:
            profile = UserProfile.objects.get(id=id)
        customer_form = CustomerGuestAccountForm(request.POST,instance = profile)
        if customer_form.is_valid():
            customer_form.save()
            return JsonResponse({"success":True,'message' : 'accepted'})
        else:
            return JsonResponse({"success":False,'message' :[(k, v[0]) for k, v in customer_form.errors.items()]})