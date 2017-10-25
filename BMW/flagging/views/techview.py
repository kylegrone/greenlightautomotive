
'''
Created on Dec 30, 2015

@author: mjnasir
'''
from django.shortcuts import render

from flagging.services.RoServices import RoServices
from dealership.models import *
from django.http.response import HttpResponse
#from flagging.factory import RoServicesFactory


def tech_view(request):
    
#     obj = {"test" : "test"}
    param = {}
    if "roNumber" in request.GET:
        roService = RoServices(request.session["dealer_id"])
        appointmentService = roService.getCustomerServiceRequest(request.GET)
        inspection = roService.getCustomerInspectionRecommendation(request.GET.get("roNumber"))
        roHeadingObject =  roService.getROdetails(request.GET.get("roNumber"))
        param = {
                 "roNumber" : request.GET.get("roNumber"),
                 "service" : appointmentService,
                 "roDetails" : roHeadingObject,
                 "color" : roService.getColorForRO(request.GET.get("roNumber")),
                 "inspection" : inspection
                 
                 }
    return render(request,"flagging_app/techview.html",param)
def edit_recommendation(request):
    try:
        id = request.GET.get("id")
        repair = AppointmentRecommendation.objects.get(id = id)
        action_plan = None
        if "action_plan" in request.GET:
            action_plan = True 
        if "parts" in request.GET:
            repair.parts = float(request.GET.get("parts"))
            
        if "labor" in request.GET:
            repair.labor = float(request.GET.get("labor"))
        repair.price =  repair.parts + repair.labor
        repair.save()
    except Exception as e:
        pass
    ro_number = repair.appointment.ro.ro_number
    inspection = RoServices(request.session["dealer_id"]).getCustomerInspectionRecommendation(ro_number)
    
    return render(request,"flagging_app/partial/recommendation.html",{"inspection" : inspection,"action_plan" : action_plan})