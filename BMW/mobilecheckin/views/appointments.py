'''
Created on Nov 28, 2015

@author: aroofi
'''
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import render

from customer.factories import CustomerServicesFactory
from customer.forms import GuestccountForm
from dealership.decorators import *
from dealership.factories import DealerShipServicesFactory
from dealership.services.appointmentservices import AppointmentService
from dealership.services.repairservices import RepairService
import json as mainjson
from mobilecheckin import confg
from mobilecheckin.decorators import *
from mobilecheckin.forms import WalkinForm


# Create your views here.
appointments_template = 'mobilecheckin/appointments/'
base_template = 'mobilecheckin/'

@checkin_access_check
def index(request):
    """
    Index
    *main page after dealer logged in
    """
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    service = dealer_factory.get_instance("vehicle")#Vehicl
#     vehichles = service.get_vehichles()
    
#     dealer_service = dealer_factory.get_instance("dealership")
    dealer_service = dealer_factory.get_instance("dealership")
    vehicle_service = dealer_factory.get_instance("vehicle")
    dealer = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    vehichles = service.get_vehichles_dealer(dealer)
    walkin = GuestccountForm()
    aptservice = AppointmentService()
    status = aptservice.get_appointments_status()
    wayaway = aptservice.get_wayaway()
    template_name = appointments_template+'index.html'
    vehicles = list(vehichles)
    config = {"dealer_id":request.session["dealer_id"],
              "dealer_code":request.session["dealer_code"],
              "CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
              "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET}
    
    
    return render(request, template_name, {'config':config, "vehicles":mainjson.dumps(vehicles),
                                           
                                           'status':status['data'], 'wayaway':wayaway['data'], 'walkinform' :walkin, 'dealer_code':request.session["dealer_code"]})

@checkin_access_check
def appointment_update(request):
    context = {}
    if request.method == 'POST': 
        data = {}
        for key, value in request.POST.iteritems():
            data[key] = value
        aptservice = AppointmentService()
        context = aptservice.update_appointment(data)  
    return JsonResponse(context)
@checkin_access_check
def remove_service(request):
    context={}
    if request.method == 'POST':
        id =  request.POST.get('id')
        rs = RepairService()
        context['deleted'] = rs.remove_service(id)
        
    return JsonResponse(context)
        