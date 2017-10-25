'''
Created on Nov 29, 2015

@author: mjnasir
'''
#from aetypes import template

from datetime import date, datetime
import pytz

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, HttpResponseRedirect, \
    HttpResponse
from django.shortcuts import render
from django.template import Context, Template

import dealership
from dealership.models import Flags, RO
from dealership.services.appointmentservices import AppointmentService
from flagging import Constants
from flagging.decorators import technician_group_check, flagger_access_check
from flagging.services.RoServices import RoServices
from django.core.paginator import  EmptyPage, PageNotAnInteger
from dealership.services.paginator import DiggPaginator as Paginator

#from pip._vendor.requests.models import json_dumps
# from flagging.factory import RoServicesFactory
#@user_passes_test(technician_group_check,login_url=Constants.REDIRECT_URL)
@flagger_access_check
def index(request):
    ro = RoServices(request.session["dealer_id"])
    template_params = ro.getAllFlagsDealer(request.session["dealer_id"])
    template_params["user"] = request.user
    template_params["dealer_code"]  =request.session["dealer_code"]
    return render(request,"flagging_app/base.html",template_params)


def ro_list_ajax(request):
#     return render(request,"flagging_app/search_header.html")
    return HttpResponseRedirect(reverse("flagging:search_ros"))
 
def search_ros_ajax(request):
    filter_dict = {}
    value = ""
    type = ""
    temp_params = {"isOrdered" : False}
    page = request.GET.get("page",1)
    try:
        filter_dict['status'] = request.GET.get("status","active")
        if "roNumber" in request.GET:
            value = filter_dict['ro_number'] = request.GET.get("roNumber")
            type = "roNumber"
        elif "advisor" in request.GET:
            value = filter_dict['advisor'] = request.GET.get("advisor")
            type = "advisor"
        elif "flags" in request.GET:
            value = filter_dict['flags'] = request.GET.get("flags")
            type = "flags"
        temp_params["orderBy"] = filter_dict["orderBy"] = request.GET.get("orderBy","ro_date")
        temp_params["isOrdered"] = True
        temp_params["order"] = filter_dict["order"]  = request.GET.get("order","desc")
#         if page == 1:
        temp_params["order"] = "asc" if filter_dict["order"] == "desc" else "desc"
    #     if request.GET.get("order"):
    #         filter_dict["order"] = request.GET.get("order")
    #         temp_params["isOrdered"] = True
    #         temp_params["order"] = request.GET.get("order")
    #         if page == 1:
    #             temp_params["order"] = "asc" if request.GET.get("order") == "desc" else "desc"
        ro_services = RoServices(request.session["dealer_id"])
        ro = ro_services.getRos(filter_dict)
   
        paginator = Paginator(ro, 25)
        ro = paginator.page(page)
    
        
    except PageNotAnInteger:
        ro = paginator.page(1)
    except EmptyPage:
        ro = paginator.page(paginator.num_pages)
    if len(ro) == 1:
            temp_params["roDetails"] = ro_services.getROdetails(ro[0].ro.ro_number)
            temp_params["color"] = ro_services.getColorForRO(ro[0].ro.ro_number)
    temp_params["ro_list"] = ro
    temp_params["ro_number"] = value
    temp_params["status"] =  request.GET.get("status","active")
    temp_params["type"] = type    
    temp_params["page"] = page
    return render(request,"flagging_app/ro_list.html",temp_params)



def update_flags(request):
    var = ""
    if request.method == "GET":
        appointment =  RoServices(request.session["dealer_id"]).get_updated_flags_appointment(request)
    return render(request,"flagging_app/partial/ro_row_data.html",{"appointment" : appointment})


def get_shop_notes(request):
    notes = None
    template_name ="flagging_app/shop_notes.html"
    roService = RoServices(request.session["dealer_id"])
    if request.method == "GET":
        notes,roObject = roService.getShopNotes(request.GET)
        
        
        if roObject !=None:
                roNumber = roObject.ro_number
        else :
            roNumber = request.GET.get("ro_number") if "ro_number" in request.GET else ""
        
            
#     if "ajaxRequest" in request.GET:
#         template_name = "flagging_app/shop_notes_ajax.html"
    
    return render(request,template_name,{"notes" : notes,"roNumber":roNumber,"ro" : roObject,"roDetails" : roService.getROdetails(roNumber)})


def add_note(request):
#     notes = None
#     ro_number =request.GET.get()
    roNumber = ""
    
    if request.method == "POST":
        
        notes,roObject = RoServices(request.session["dealer_id"]).addNote(request.POST, request.user)
        roNumber = roObject.ro_number
    return HttpResponseRedirect( reverse('flagging:shop_notes')+"?ro_number=" +roNumber)


def get_flag_to_update_type(request):
    json = {}
    if "roId" in request.GET:
        roId = int(request.GET.get("roId"))
        ro = RoServices(request.session["dealer_id"])
        
        json = {"nextFlag" : ro.getFlagToUpdateType(roId)}
    return JsonResponse(json)

#     return render(request,template_name,{"notes" : notes,"ro" : roObject})
def get_ro_details_ajax(request):
    if "roId" in request.GET:
        try:
            roService =RoServices(request.session["dealer_id"])
            ro = RO.objects.get(id=int(request.GET.get("roId")))
            roDetails = roService.getROdetails(ro.ro_number)
            color = roService.getColorForRO(ro.ro_number)
            return render(request,"flagging_app/partial/ro_details.html",{"roDetails" : roDetails})
        except Exception as e :
            return ""
    
def get_flag_notes(request):
#     print "asdfasd"
    notes = ""
    if request.method == "GET":
        id = int(request.GET.get("flagId"))
        notes = Flags.objects.get(id=id).notes
    return  HttpResponse(notes)  

def add_recommendations(request):
    RoServices(request.session["dealer_id"]).addRecommendations(request)
    return HttpResponse(RoServices().get_updated_flags_appointment(request))
def mark_as_complete(request):
    ro_id = request.GET.get("ro_id")
    ro = RO.objects.get(id=ro_id)
    ro.ro_completed =  datetime.now(pytz.utc)  
    ro.save()
    return HttpResponseRedirect(reverse("flagging:search_ros"))
