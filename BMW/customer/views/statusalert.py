import json

from django.core.mail import send_mail
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from customer.factories import CustomerServicesFactory
from customer.services.paypal import paypal_payment
from dealership.models import *
from django.contrib.sites.shortcuts import get_current_site
from dealership.factories import DealerShipServicesFactory

def index(request,appointment_id):
    customer_factory = CustomerServicesFactory()
    
    service = customer_factory.get_instance("user")
    
    templates = "customer/statusalert/index.html"
    try:
        appt_details = Appointment.objects.get(id = appointment_id)
    except Appointment.DoesNotExist:
        raise Http404
    flages = Flags.objects.filter(type=3, customer_facing=True, dealer_id = appt_details.dealer.id)
    recmndations = AppointmentRecommendation.objects.filter(appointment_id = appointment_id)
    
    total = 0
    for obj in recmndations:
        total += obj.price 
        
    appt_services = AppointmentService.objects.filter(appointment_id=appointment_id)
    if appt_details:
        userprofile = appt_details.customer
#     userprofile =service.get_userprofile(request.user)
    service_total = 0
    for obj in appt_services:
        service_total += obj.price
    approved_recmm = AppointmentRecommendation.objects.filter(appointment_id=appointment_id , status = "Accept")
    for obj in approved_recmm:
        service_total += obj.price
    dealer = appt_details.dealer
    dealer_code=None
    if dealer:
        dealer_code = dealer.dealer_code
        
    context  = {'flages':flages , 'appt' : appt_details , 'recommandations' : recmndations , 'total':total,
                                     'appt_services' : appt_services , 'approved_rec' : approved_recmm , 's_total':service_total,'dealer_code':dealer_code}
    service.set_centrifuge_context(request,dealer_code,userprofile, context,chatposition="top")
    return render(request,templates,context)

@csrf_exempt
def approve_recomandations(request,appointment_id):
    if request.method == "POST":
        email_data =[]
        data = json.loads(request.POST['data'])
        for obj in data:
            app_rec = AppointmentRecommendation.objects.get(id = obj['id'])
            app_rec.status = obj['val']
            app_rec.save()
            status_dic={"name": app_rec.notes ,"part_price":app_rec.parts,"labour_price":app_rec.labor,"price":app_rec.price, "status":app_rec.status}
            email_data.append(status_dic)
        appnt = Appointment.objects.get(id=appointment_id)
        appnt.appointment_recommandation_status = True
        appnt.save()
        if request.POST['email_check'] == "true":
            dealer_factory = DealerShipServicesFactory()
            notificationservice = dealer_factory.get_instance("notification")
            context = {'status' : email_data }
            params = json.dumps(context)  
            try:
                notificationservice.send_dealer_based_notification(appnt.dealer,appnt.customer,params,"recommendation_status_details",send_email=True,send_text=False)
            except Exception,e:
                print e 
            #msg_plain = render_to_string('customer/emails/approve_details.txt',context)
            #msg_html = render_to_string('customer/emails/approve_details.html', context)
            #send_mail('Recommandation Details', msg_plain , settings.EMAIL_HOST_USER , [appnt.customer.email_1 , appnt.customer.email_2] ,html_message=msg_html, fail_silently=False)

    
        return HttpResponse(json.dumps({'message' : 'Status Marked'}))


@csrf_exempt
def reply(request,appointment_id):
    if request.method == "POST":
        try:
            appt = Appointment.objects.get(id = appointment_id)
        except Appointment.DoesNotExist:
            raise Http404
        if not appt.dealer:
            raise Http404
        service_total = 0
        appt_services = AppointmentService.objects.filter(appointment_id=appointment_id)
        list_service = []
        list_recommandation = []
        for obj in appt_services:
            service_total += obj.price
            list_service.append(obj)
        approved_recmm = AppointmentRecommendation.objects.filter(appointment_id=appointment_id , status = "Accept")
        for obj in approved_recmm:
            service_total += obj.price
            list_recommandation.append(obj)
        payment = paypal_payment(appt.dealer)
        message = None
        url = None
        domain = get_current_site(request).domain
        if appt.creditcard_id:
            result = payment.paywith_creditcard_token(appt.creditcard_id,list_service,list_recommandation,service_total)
            if 'id' in result:
                appt.payment_id = result['id']
                appt.payment_status = True
                appt.save()
                flag = Flags.objects.get(id=appt.dealer.prestagevehicle_flag_id)
                date = timezone.now()
                appt.ro.flag3 = flag
                appt.ro.flag3_updated_time = date
                appt.ro.save()
                message = "Thankyou For your Payment ,your payment id is " + result['id']+". Your Auto will be ready for pick-up soon."
            else:
                url = payment.paywith_paypal(list_service,list_recommandation,service_total,appointment_id,domain)
                message = "Your payment encounter some error" + result['error']+ ". <a href="+url+">Click Here</a> to process your payment manually."
        else:
            url = payment.paywith_paypal(list_service,list_recommandation,service_total,appointment_id,domain)
        
    return HttpResponse(json.dumps({'message' : message , 'data' : url }))



def payment(request,appointment_id):
    templates = "customer/statusalert/payment.html"
    payment_id = request.GET['paymentId'] 
    payer_id = request.GET['PayerID']
    try:
        appt = Appointment.objects.get(id= appointment_id)
    except Appointment.DoesNotExist:
        raise Http404
    if not appt.dealer:
        raise Http404
    payment = paypal_payment(appt.dealer)
    if payment_id and payer_id :
        pay_id  = payment.execute(payment_id, payer_id)
        if 'id' in pay_id:
            appt.payment_id = pay_id['id']
            appt.payment_status = True
            appt.save()
            flag = Flags.objects.get(id=appt.dealer.prestagevehicle_flag_id)
            date = timezone.now()
            appt.ro.flag3 = flag
            appt.ro.flag3_updated_time = date
            appt.ro.save()
            message = "Thankyou For your Payment ,your payment id is " + pay_id['id']+". Your Auto will be ready for pick-up soon."
        else:
            message = "Your payment encounter some error" + pay_id['error']
    else:
        message= "Invalid Request" 
    return render(request,templates,{'message' : message})