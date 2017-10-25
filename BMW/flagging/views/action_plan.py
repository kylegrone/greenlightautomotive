import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import Context, Template
import pdfcrowd

from customer.services.userservices import CUserService
from dealership.models import Appointment, Dealer
from dealership.services import userservices
from dealership.services.notificationservice import NotificationService
from flagging.services.RoServices import RoServices
from oauth2client.client import SETTINGS
from django.conf import settings

def action_plan(request):
    params ={}
    if request.method == "GET":
        if "roNumber" in request.GET:
            roNumber = request.GET.get("roNumber")
            
            ro = RoServices(request.session["dealer_id"])
            params['service'] = ro.getCustomerServiceRequest(request.GET)
            params['summary'] = ro.getSummaryDetailsByRoNumber(roNumber)
            params['roDetails'] = ro.getROdetails(roNumber)
            params['color'] = ro.getColorForRO(roNumber)
            params['roNumber'] = roNumber
            params['recommendations'] = ro.getInspectionRecommendationSummary(roNumber)
            params["inspection"] = ro.getCustomerInspectionRecommendation(roNumber)
            params["action_plan"] = "true"
    return render(request,"flagging_app/action_plan.html",params)




def generate_pdf_view(request):
    try:
        # create an API client instance
        client = pdfcrowd.Client("mjnasir", "a90dfc17a16777af1087a5b00e88b5c2")

        # convert a web page and store the generated PDF to a variable
        ro_number = request.GET.get("ro_number")
        dealer_id = request.session["dealer_id"]
        url = request.GET.get("url")
#         url_str = "https://greenlightautomotive.com/app/flagger/action_plan_pdf/?roNumber=" +str(ro_number)+"&dealer_code=infiniti-0134&dealer_id="+str(dealer_id)
        
        url_str = settings.SITE_MAIN_URL+ reverse("flagging:action_plan_pdf") + "?roNumber=" +str(ro_number)+"&dealer_id="+str(dealer_id)
        print url_str
        pdf = client.convertURI(url_str)
#         render(request,"flagging_app/action_plan_pdf")
         # set HTTP response headers
        response = HttpResponse(content_type="application/pdf")
        response["Cache-Control"] = "max-age=0"
        response["Accept-Ranges"] = "none"
        response["Content-Disposition"] = "attachment; filename=action_plan.pdf"

        # send the generated PDF
        response.write(pdf)
    except pdfcrowd.Error, why:
        print why
        response = HttpResponse(mimetype="text/plain")
        response.write(why)
    return response

def email_action_plan(request):
    try:
        userservice = CUserService()
        notfication_service = NotificationService()
        ro_number = request.GET.get("ro_number")
        dealer_id = request.session["dealer_id"]
        dealer = Dealer.objects.get(id=dealer_id)
        url = request.GET.get("url")
        final_url = url + reverse("flagging:action_plan_pdf") + "?roNumber=" + ro_number + "&dealer_id="+str(dealer_id)
        appt = Appointment.objects.get(ro__ro_number = ro_number)
        emails = userservice.get_profile_emails(appt.customer)
        
        if len(emails)>0:
            email = emails[0]
            print final_url
#             userservices.UserService().sendEmailPDf(email, final_url)
            notfication_service.send_dealer_based_notification(dealer,appt.customer,json.dumps({"final_url":final_url}),"action_plan",send_email=True,send_text=False)
            return HttpResponse("200")
            
             
        else:
            return HttpResponse("404")
    except Exception,e:
        return HttpResponse("400")

def action_plan_pdf(request):
        params ={}
        if request.method == "GET":
            if "roNumber" in request.GET:
                roNumber = request.GET.get("roNumber")
                ro = RoServices(request.GET.get("dealer_id"))
                params['service'] = ro.getCustomerServiceRequest(request.GET)
                params['summary'] = ro.getSummaryDetailsByRoNumber(roNumber)
                params['roDetails'] = ro.getROdetails(roNumber)
                params['color'] = ro.getColorForRO(roNumber)
                params['roNumber'] = roNumber
                params['recommendations'] = ro.getInspectionRecommendationSummary(roNumber)
                params["inspection"] = ro.getCustomerInspectionRecommendation(roNumber)
                params["action_plan"] = "true"
                apt = Appointment.objects.get(ro__ro_number = roNumber)
                first_name = apt.customer.first_name if apt.customer.first_name else " "
                last_name = apt.customer.last_name if apt.customer.last_name else " " 
                params["vehicle_vin"] = apt.vehicle.vin_number
                params["customer"] = first_name + " " + last_name
                params["dealer_code"] = Dealer.objects.get(id=request.GET.get("dealer_id")).dealer_code
        return render(request,"flagging_app/action_plan_pdf.html",params)
       