import base64
import cStringIO
import os

from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core import serializers
from dealership.services.paginator import DiggPaginator as Paginator
from django.core.paginator import  PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, HttpResponseRedirect, \
    HttpResponse, Http404
from django.shortcuts import render
import pytesseract

from customer.app_confg import confg
from customer.decorators.decorators import customer_group_check, \
    dealership_required_or_logged_in
from customer.factories import CustomerServicesFactory
from customer.forms import CustomerVehichleForm, CustomerAccountForm
from dealership.factories import DealerShipServicesFactory
from dealership.models import UserProfile
import json as mainjson
from livechat.forms import UploadForm


@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)
def service_history(request,vehicle_id):
    
    template_name = 'customer/vehicle_services.html'
    user = request.user
#     user = User.objects.get(id=user.id)
    profile = UserProfile.objects.get(user_id=user.id)
    dealer_code = request.session["dealer_code"]
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    appt_service = dealer_factory.get_instance("appointment")#DealerShipService()
    
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    
    
    appts_list = appt_service.get_old_appointments_by(vehicle_id,dealership)
    paginator = Paginator(appts_list, 10)
    page = request.GET.get('page',1)
    try:
        appts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        appts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        appts = paginator.page(paginator.num_pages)
        
    context = {"appts":appts,"dealer_code":dealer_code,"vehicle_id":int(vehicle_id)}
    return render(request, template_name,context)

@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)
@dealership_required_or_logged_in
def mainview(request,dealer_code,profile):
    """
            This is the main screen after login. It is used to display the vehicles and also
            the add form form for vehicle
    """
    
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    name = request.user.first_name+" "+request.user.last_name
    service = dealer_factory.get_instance("vehicle")#VehicleService()
    template_name = 'customer/customer_vehicle.html'
    userservice = customer_factory.get_instance("user")#CUserService()
#     vehichles = service.get_vehichles()
    vehichles = service.get_vehichles_dealer(dealership)
    profile = userservice.get_userprofile(request.user)
    customer_vehicles = service.get_customer_vehicles(profile.id,dealership)
    
    vehicles = list(vehichles)
    media_url = settings.MEDIA_URL
    tab = ""
    myadvisor = None
    if profile:
        myadvisor = userservice.get_my_advisor(profile.id,dealership.id)
    if request.method == 'POST':
        vehicle_form = CustomerVehichleForm(request.POST)
        if vehicle_form.is_valid():
            try:
                vehicle_form.save()
                if request.POST.get("vin_data")!=None and request.POST.get("vin_data")!="":
                    service.save_vehicle_vin_data(vehicle_form.instance,request.POST.get("vin_data"))
                messages.success(request, "Vehicle added successfully")
                return HttpResponseRedirect(reverse("customer:main"))
            except:
                vehicle_form.add_error(None,"Some error occured while saving")
    else:
        
        vehicle_form = CustomerVehichleForm(initial={'user': profile.id})
        
        
    
    context = {"page_title":"Customer Profile",
                                          "vehicle_form":vehicle_form,
                                          "media_url":media_url,'name':name,
                                          "vehicles":mainjson.dumps(vehicles),
                                          "customer_vehicles":customer_vehicles,
                                          "tab":tab,
                                          'acitve' : True,
                                          "dealer_code":dealer_code,
                                          "profile":profile,
                                          "myadvisor":myadvisor,"request":request
#                                           "userprofile":userservice.get_userprofile(request.user)
                                         
                                          }
    userservice.set_centrifuge_context(request, dealer_code,profile,context,chatposition="top")
    return render(request, template_name,context)
    

        
         

 
   
@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)
@dealership_required_or_logged_in   
def del_vehicle(request,dealer_code,profile):
    """
        this request is used to delete the vehicle
    """ 
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.GET.get("vehicle_id"):
        vid = request.GET.get("vehicle_id")
        service = dealer_factory.get_instance("vehicle")#VehicleService()
        if service.user_allowed_delete(vid,request.user.userprofile.id):
            service.delete_customer_vehicle(vid)
            messages.success(request, "Vehicle delete successfully")
        else:
            messages.error(request, "User not allowed to delete vehicle","danger")
        return HttpResponseRedirect(reverse("customer:main"))
        
        
# from customer.forms import CustomerVehichleForm
def get_vehicle(request):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    resp = {}
    make = request.GET.get("make")
    model = request.GET.get("model")
    trim = request.GET.get("trim")
    year = request.GET.get("year")
    service= dealer_factory.get_instance("vehicle")#VehicleService()
    vehicles = service.get_vehichles(make, model, trim, year, 1)
#     vehicles = serializers.serialize('json', vehicles)
    resp["success"] = True
    resp["media_url"] =   settings.MEDIA_URL
    resp["vehicles"] =  list(vehicles)
    return JsonResponse(resp,safe=False)
  
    

def ocr_snap(request):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.POST.get("imgBase64")!=None:
        cameraservice  = customer_factory.get_instance("camera")#CameraService()
        img = cameraservice.get_image_from_base64(request.POST.get("imgBase64"))
        print img
        qr_text = cameraservice.get_zbar_from(img)
#         qr_text = "baAe"
        return JsonResponse({"resp":qr_text})
        
    

