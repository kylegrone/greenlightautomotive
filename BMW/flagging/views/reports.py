'''
Created on Jan 21, 2016

@author: mjnasir
'''
from cgi import escape

from django import template
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.template.context import Context
from django.template.loader import get_template

from xhtml2pdf import pisa


import cStringIO as StringIO

from dealership.models import RO
from flagging.services.RoServices import RoServices,Reports


def get_reports(request):
#     return HttpResponseRedirect(reverse("flagging:flag_analysis"))
    return render(request,"flagging_app/reports_tab.html")


def get_shop_flag_report(request):
    
    return HttpResponse("")
#     rows = RoServices().getShopFlagAnalysisReport()
#     if "download" in request.GET:
#         context = Context({"rows" : rows})
#         template = get_template("flagging_app/reports.html")
#         html  = template.render(context)
#         result = StringIO.StringIO()
#     #     html=render(request,"flagging_app/reports.html",{"rows" : rows})
#     
#         pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#         if not pdf.err:
#             return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return render(request,"flagging_app/reports.html",{"rows" : rows})


def get_repair_order_list(request):
    RoServices().get_repair_order_list("", "", "")
    
def generate_report(request):
    report_type = int(request.GET.get("report_type"))
    ro_number = request.GET.get("ro_number")
    dealer_id =request.session["dealer_id"]
    reports = Reports(dealer_id)
    params={}
    template_name=""
    if report_type == 1:
        params["rows"] = reports.get_technician_analysis_report()
        template_name = "flagging_app/tech_analysis_report.html"
    elif report_type == 2:
        params["rows"] = reports.getShopFlagAnalysisReport(ro_number)
        template_name = "flagging_app/reports.html"
    elif report_type == 3:
        params["rows"] = reports.get_service_advisor_report()
        template_name = "flagging_app/service_advisor_report.html"
    elif report_type ==4:
        params["rows"] = reports.get_repair_order_list(ro_number, "", "")
        template_name = "flagging_app/ro_list_report.html"
    return render(request,template_name,params)