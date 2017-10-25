'''
Created on Jan 1, 2016

@author: mjnasir
'''
import json

from django.core import serializers
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa

import cStringIO as StringIO
from dealership.models import RoInspection, RO, InspectionCatagories, \
    InspectionPackage
from flagging.services.RoServices import RoServices


def inspection(request):
    params = {}
    ro = RoServices(request.session["dealer_id"])
    dealer_id = request.session.get("dealer_id")
    _request = request.GET
    if request.method == "POST":
        _request = request.POST
        ro.processInspectionFields(request)
    ro_number = _request.get("ro_number","")
    default_package = InspectionPackage.objects.filter(dealer=ro.dealer)
    params["selected_package"] = package =   _request.get("package",None if len(default_package) < 1 else default_package[0].package)
    params["category_items"] = categories_items_dict = ro.get_inspection_data(ro_number,package,dealer_id)
    params["ro_number"]= ro_number
    params["packages"] = ro.get_all_packages()
    params["name"] = "%s, %s" % (request.user.last_name,request.user.first_name) 
    params["summary"] = ro.getSummaryDetailsByRoNumber(ro_number,package)
    params["roDetails"] = ro.getROdetails(ro_number)
    return render(request,"flagging_app/inspection_new.html",params)


def get_results_summary_pdf(request):
    ro_number = request.GET.get("roNumber")
    package = request.GET.get("package",None)
    summary = RoServices().getSummaryDetailsByRoNumber(ro_number,package)
    template = get_template("flagging_app/inspection_pdf.html")
    url = settings.SITE_MAIN_URL
    html  = template.render({"url":url,"result_summary" : summary})
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors while creating PFD')


def get_results_summary(request):
    params = {}
    if "roNumber" in request.GET:
        roNumber = request.GET.get("roNumber")
        params["summary"] = RoServices().getSummaryDetailsByRoNumber(roNumber)
    return render(request,"flagging_app/result_summary.html",params)
def add_inspection_record(request):
    
    description = request.GET.get("description")
    type = request.GET.get("type")
    roNumber = request.GET.get("roNumber")
    ro = RO.objects.get(ro_number = roNumber)
    inspectionCatagory = InspectionCatagories()
    inspectionCatagory.ro = ro
    inspectionCatagory.description = description
    inspectionCatagory.type = type
    inspectionCatagory.save()
    params = {"id" : inspectionCatagory.id,
              "type" : inspectionCatagory.type,
              "description": inspectionCatagory.description,
              "roNumber" : roNumber
              }
    return render(request,"flagging_app/add_inspection.html",params)

def inspection_test(request):
    dealer_id = request.session["dealer_id"]
    ro_number = request.GET.get("ro_number")
    package = request.GET.get("package")
    categories_items_dict = RoServices().get_inspection_data(ro_number,package,dealer_id)
    return render(request,"flagging_app/inspection_new.html",{"category_items":categories_items_dict})
