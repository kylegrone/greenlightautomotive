from base64 import b64decode
import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from customer.factories import CustomerServicesFactory
from customer.forms import GuestccountForm
from dealership.decorators import *
from dealership.factories import DealerShipServicesFactory
from dealership.models import *
from mobilecheckin import confg
from mobilecheckin.services.walkinservice import WalkinService


@csrf_exempt
def create_appointment(request):
    print request.POST,"######################"
    try:
        advisor_user = request.user
       
        customer_factory = CustomerServicesFactory()
        dealer_factory = DealerShipServicesFactory()
        dealer_service = dealer_factory.get_instance("dealership")
        uservice = customer_factory.get_instance("user") #CUserService()
        capacity_service = dealer_factory.get_instance("capacity")
        appt_service = dealer_factory.get_instance("appointment")
        if request.method=="POST":
            now = timezone.now()
            try:
                shophrs = ShopHours.objects.get(day = now.strftime('%A') , shop_id = request.session['dealer_id'] )
            except Exception,e:
                return JsonResponse({'success':False,'message' : 'Dealership is closed'})
            open_time = timezone.make_aware(datetime.datetime.combine(datetime.date.today(), shophrs.time_from))
            closing_time =  timezone.make_aware(datetime.datetime.combine(datetime.date.today(), shophrs.time_to))
            dealer = dealer_service.get_dealer_by_id(request.session['dealer_id'] )
            if now > closing_time:
                return JsonResponse({'success':False,'message' : 'Dealership is closed'})
            else:
                profile_id = request.POST.get('customer_id')
                if profile_id:
                    user = UserProfile.objects.get(id=profile_id)
                    slab_date = timezone.make_aware(datetime.datetime.today())
                    slabs = capacity_service.get_available_slabs_for(slab_date,dealer,None) 
                    
                    if len(slabs)>0:
                        slab = slabs[0]  
                        vehicle = Vehicle.objects.get(id =request.POST['vehicle_id'] )
                        cv = None
                        try:
                            cv = CustomerVehicle.objects.filter(user = user,vehicle = vehicle,vin_number = request.POST['vin']).first()
                        except CustomerVehicle.DoesNotExist:
                            cv = None
                        if cv ==None:
                            cv= CustomerVehicle(user = user , vehicle = vehicle ,vin_number = request.POST['vin'])
                            cv.save()
                        slab_time = datetime.datetime.strptime(slab["value"], '%Y-%m-%d %H:%M')
                        slab_time = timezone.make_aware(slab_time)
                        appt_save = appt_service.save_appoitment_with(slab_time,advisor_user.id,1,user.id,None,None,dealer_id=dealer.id)
                        appt_save.vehicle = cv
                        appt_save.save()
                        if appt_save==False:
                            return JsonResponse({"success":False,'message' : 'Error Occured While Booking Appointment'})
                    else:
                        return JsonResponse({"success":False,'message' : 'No Slot Available'})
                
                    return JsonResponse({"success":True,'message' : 'accepted'})
                else:
                    phone_number = request.POST.get("phone_number_1")
                    email = request.POST.get("email_1")
                    profile = uservice.get_user_profile_by_phone(phone_number)
                    if profile ==None:
                        profile = uservice.get_user_profile_by_email(email)
                    if profile ==None:
                        profile = UserProfile()
                    customer_form = GuestccountForm(request.POST,instance = profile)
                    if customer_form.is_valid():
                        slab_date = timezone.make_aware(datetime.datetime.today())
                        slabs = capacity_service.get_available_slabs_for(slab_date,dealer,None) 
                        if len(slabs)>0:
                            slab = slabs[0]
                            profile = customer_form.save()    
                            vehicle = Vehicle.objects.get(id =request.POST['vehicle_id'] )
                            cv = None
                            try:
                                cv = CustomerVehicle.objects.filter(user = profile,vehicle = vehicle,vin_number = request.POST['vin']).first()
                            except CustomerVehicle.DoesNotExist:
                                cv = None
                            if cv ==None:
                                cv= CustomerVehicle(user = profile , vehicle = vehicle ,vin_number = request.POST['vin'])
                                cv.save()
                                
                            slab_time = datetime.datetime.strptime(slab["value"], '%Y-%m-%d %H:%M')
                            slab_time = timezone.make_aware(slab_time)
                            appt_save = appt_service.save_appoitment_with(slab_time,advisor_user.id,1,profile.id,None,None,dealer_id=dealer.id)
                            appt_save.vehicle = cv
                            appt_save.save()
                            if appt_save==False:
                                return JsonResponse({"success":False,'message' : 'Error Occured While Booking Appointment'})
                        else:
                            return JsonResponse({"success":False,'message' : 'No Slot Available'})
                    else:
                        return JsonResponse({"success":False,'message' :[(k, v[0]) for k, v in customer_form.errors.items()]})
                    return JsonResponse({"success":True,'message' : 'accepted'})
    except Exception,e:
        print e
        print "Exception"
        return JsonResponse({"success":False, 'message' : 'Error Occured while Booking Appointment'})
    
@csrf_exempt    
def searchuser(request):
    if request.method == "POST":
        wlkin = WalkinService()
        phone = request.POST['phone']
        user = wlkin.search_customer(phone)
        if user:
            vehicles = wlkin.customer_vehicles(user[0])
            return JsonResponse({"success":True,'customer' : {'id': user[0].id , 'fname' : user[0].first_name ,
                                                               'lname' : user[0].last_name , 'email' : user[0].email_1,'phone':phone , 'vehicles':vehicles}})
        else:
            return JsonResponse({"success":False})
                
        