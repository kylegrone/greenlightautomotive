import datetime

from PIL import Image
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone

from BMW import settings
from customer.app_confg import confg
from customer.decorators.decorators import dealership_required, dealership_required_or_logged_in, \
    appointment_required, customer_group_check
from customer.factories import CustomerServicesFactory
from customer.forms import CustomerVehichleForm, CustomerAccountForm, \
    GuestccountForm, UploadVinForm
from dealership.factories import DealerShipServicesFactory
from dealership.forms import LoginForm, CreateUserForm
from dealership.models import CustomerVehicle, UserProfile, Appointment
import json as mainjson


@appointment_required
@dealership_required_or_logged_in
def get_cart(request,dealer_code,profile,appointment):
    try:
        if appointment:
                
                customer_factory = CustomerServicesFactory()
                dealer_factory = DealerShipServicesFactory()
                dealer_service = dealer_factory.get_instance("dealership")
                dealer = dealer_service.get_dealer_by(dealer_code)
                userservice = customer_factory.get_instance("user")
                appointmentservice = dealer_factory.get_instance("appointment")
                repairservice = dealer_factory.get_instance("repair")
                services = repairservice.get_service_for(appointment.id,'s')
                repairs = repairservice.get_service_for(appointment.id,'r')
                print services
                print repairs
               
                context = {
                                        "mainurl":settings.MEDIA_ROOT,
                                          "appointment":appointment,
                                          "dealer_code":dealer_code,
                                          "services":services,"repairs":repairs,
                                          "cart_count":len(repairs)+len(services)
            
                }
   
                return render(request, "customer/cart/main.html",context)
        else:
#             return ""
            return render(request, "customer/cart/main.html",{})
    except Exception,e:
        print e
            