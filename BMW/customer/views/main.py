import os

from PIL import Image
from cent.core import Client
from centrifuge import client
from django.conf import settings
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import pytesseract

from customer.app_confg import confg
from customer.decorators.decorators import customer_group_check, \
    dealership_required
from customer.services.cameraservice import CameraService
from dealership import forms
from dealership.models import Dealer
from dealership.services.pusherservice import PusherService
from dealership.services.vehicleservices import VehicleService


# from customer.forms import CustomerVehichleForm
# Create your views here.
def test_ocr(request):
        cameraservice = CameraService()
        media_root= settings.MEDIA_ROOT
        image = Image.open(media_root+'/medianewtest.png')
        text = cameraservice.get_zbar_from(image)
        print text
#     pushr = PusherService()
#     connect = pushr.connect(settings.CENTRIFUGE_API_URL, settings.CENTRIFUGE_SECRET)
#     pushr.update_clients("demo",
#                                 ["appointments"],
#                                 {"old_data":
#                                     {"name":"asim"},
#                                 "new_data":
#                                     {"name":"imran"}
#                                 }
#                          )
# 
# #      
        return JsonResponse({"test":text})

@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)
def test_puller(request):
    dealership_code = request.session["dealer_code"]
    dealer = Dealer.objects.get(dealer_code = request.session["dealer_code"])
    #dealer = Dealer.objects.get(dealer_code = "isb-0134")
   
    template_name = "customer/puller.html"
    return render(request, template_name,{"CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
                                          "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET,
                                          "dealer":dealer
                                          })
    
