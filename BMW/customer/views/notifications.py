
import base64
import cStringIO
import os

from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, HttpResponseRedirect, \
    HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
import pytesseract

from customer.app_confg import confg
from customer.decorators.decorators import customer_group_check, \
    dealership_required_or_logged_in
from customer.factories import CustomerServicesFactory
from customer.forms import CustomerVehichleForm, CustomerAccountForm
from customer.services.cameraservice import CameraService
from customer.services.userservices import CUserService
from dealership.factories import DealerShipServicesFactory
from dealership.services.dealershipservice import DealerShipService
from dealership.services.pusherservice import PusherService
from dealership.services.vehicleservices import VehicleService
import json as mainjson


@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)
@dealership_required_or_logged_in
def notificationssettings(request,dealer_code,profile):
    """
           This is the notification screen. This is used to save settings
    """
    customer_factory = CustomerServicesFactory()
    dealer_factory= DealerShipServicesFactory()
    user_service = customer_factory.get_instance("user")
    profile = user_service.get_userprofile(request.user)
    notificationservice = dealer_factory.get_instance("notification")
    remindersettings = notificationservice.get_user_remindersettings(profile,True)
    phone_numbers = user_service.get_profile_numbers(profile)
    emails = user_service.get_profile_emails(profile)
    carrier_choices =    (
                         ("Verizon"),
                         ("AT & T"),
                         
    )
    tab = "notification"
    if request.method == "POST":
        special_offer_notify = False
        if request.POST.get("special_offer_notify"):
            special_offer_notify = True
        ids =  request.POST.getlist("settings_id")
        for id in ids:
            
            textset = False
            phoneset=False
            emailset = False
            if request.POST.get("setting_email_"+id):
                emailset = True
            if request.POST.get("setting_text_"+id):
                textset=True
            if request.POST.get("setting_phone_"+id):
                phoneset=True
            notificationservice.save_reminder_settings(id,emailset,textset,phoneset)
#         user_service.save_active_phone(profile,request.POST.get("active_phone_number"))
        user_service.save_active_email(profile,request.POST.get("active_email"))
        user_service.save_special_offer_notify(profile,special_offer_notify)
        messages.success(request, "Reminder settings saved successfully")
        return HttpResponseRedirect(reverse("customer:notifications"))
        
    else:
        context = {"dealer_code":dealer_code,"tab":tab,"page_title":"Customer Profile",
                                                              "remindersettings":remindersettings,
                                                                "phonenumbers":phone_numbers,
                                                                "emails":emails,"profile":profile,"carrier_choices":carrier_choices}
        user_service.set_centrifuge_context(request, dealer_code,profile,context,chatposition="top")
        return render(request, "customer/notifications.html",context
                    )