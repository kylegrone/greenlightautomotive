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
from dealership.services.repairservices import RepairService
from dealership.services.breadcrumb import BreadCrumb

from dealership.factories import DealerShipServicesFactory

@dealership_access_check
def rservices(request):    
    dealer_factory = DealerShipServicesFactory()
    breadcrumb = BreadCrumb()    
    #form = AddServiceRepairForm()    
    breadcrumb = breadcrumb.create_breadcrumb(["rservices"])
    template = 'rservices/index.html'
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
          "tab":"rservices",
          "CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
          "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET}
    
    return render(request, template, {'config':config,
                                      "favorites":favorites,
                                      'breadcrumb':breadcrumb,
                                      'qstring':qstring})


@dealership_access_check 
def get_rservices_form(request):
    dealer_factory = DealerShipServicesFactory()
    repairservice = dealer_factory.get_instance("repair")
    dealership =  dealer_factory.get_instance("dealership")
    dealer = dealership.get_dealer_by_id(request.session["dealer_id"])
    
    template = 'rservices/partials/rservices_add_content.html'
    form = ManageServiceRepairForm(initial={"price_unit":dealer.price_unit})
    
    if request.method == 'POST':         
        if request.POST.get("id"):            
            service_instance = repairservice.get_service(request.POST.get('id'))
            form = ManageServiceRepairForm(instance=service_instance)            
    return render(request, template, {"dealer_id":request.session["dealer_id"], 'form':form})
    
@dealership_access_check   
def rservices_create_update(request):
    #context = {}
    dealer_factory = DealerShipServicesFactory()
    repairservice = dealer_factory.get_instance("repair")
    if request.method == 'POST': 
        if request.POST.get("id"):            
            print request.FILES
            service_instance = repairservice.get_service(request.POST.get('id'))
            form = ManageServiceRepairForm(request.POST, request.FILES,instance=service_instance)
        else:
            form = ManageServiceRepairForm(request.POST,request.FILES)
        if form.is_valid():
            rservice = form.save()
            return JsonResponse({"status":"success", "id":rservice.pk})
        else:
            return JsonResponse({"status":"error", "errors":form.errors})
    return JsonResponse({"id":0}) 
    """
        data = {}
        for key, value in request.POST.iteritems():
            data[key] = value
        data["dealer_id"] = request.session["dealer_id"]
        rservice = RepairService()
        context = rservice.create_update_dealer_services(data)  
    return JsonResponse(context)
    """

@dealership_access_check
def rservices_delete(request):
    id = 0
    if request.method == 'POST': 
        id = request.POST.get("id")
    else:
        id = request.GET.get("id")
        
    rservice = RepairService()
    context = rservice.delete_dealer_services(id)  
    return JsonResponse(context)