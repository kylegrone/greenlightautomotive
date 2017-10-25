

#from StdSuites.AppleScript_Suite import event
import datetime

from PIL import Image
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, Http404, JsonResponse, \
    HttpResponse
from django.shortcuts import render
from django.utils import timezone

from BMW import settings
from customer.app_confg import confg
from customer.decorators.decorators import dealership_required, dealership_required_or_logged_in, \
    appointment_required, customer_group_check
from customer.factories import CustomerServicesFactory
from customer.forms import CustomerVehichleForm, CustomerAccountForm, \
    GuestccountForm, UploadVinForm
from customer.services.gcalservice import GCalService
from dealership.factories import DealerShipServicesFactory
from dealership.forms import LoginForm, CreateUserForm
from dealership.models import CustomerVehicle, UserProfile, Appointment
import json as mainjson

def print_appointment(request):
    if request.GET.get("appointment_id"):
        customer_factory = CustomerServicesFactory()
        dealer_factory = DealerShipServicesFactory()
        appt_service = dealer_factory.get_instance("appointment") #AppointmentService()
        appointment = appt_service.get_appointment(request.GET.get("appointment_id"))
      
        return render(request, "customer/print_appointment.html",{"appointment":appointment})
        

# @dealership_required
def download_calendar(request):
    
    if request.GET.get("appointment_id"):
        
        customer_factory = CustomerServicesFactory()
        dealer_factory = DealerShipServicesFactory()
        appt_service = dealer_factory.get_instance("appointment") #AppointmentService()
        cal = appt_service.get_calendar(request.GET.get("appointment_id"))
        if cal:
            response = HttpResponse(cal.to_ical(), content_type="text/calendar")
            response['Content-Disposition'] = 'attachment; filename=%s.ics' % "appointment"
            return response
        else:
            raise Http404("No Appointment found")       


def uploadvin(request):
    """    
           This method is used to upload the images of the chat and save it to a model.
    """
    customer_factory = CustomerServicesFactory()
    resp = {"success":False,"imgurl":None}
    if request.method=="POST":
        img = UploadVinForm(request.POST, request.FILES)       
        if img.is_valid():
            imgfieds = img.save()  
            image = Image.open(imgfieds.pic)
            cameraservice  = customer_factory.get_instance("camera")#CameraService()
            qr_text = cameraservice.get_zbar_from(image)
            resp["success"] = True
            resp["imgurl"] = imgfieds.pic.url
            resp["vin"] = qr_text
            return JsonResponse(resp)
    return JsonResponse(resp)
#   
@dealership_required
def book_appointment_now_new(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    dealer = dealer_service.get_dealer_by(dealer_code)
    userservice = customer_factory.get_instance("user")
    way_away_service = dealer_factory.get_instance("wayaway")
    way_away = way_away_service.get_all_wayaway(dealer)
    uservice = customer_factory.get_instance("user") #CUserService()
    appt_service = dealer_factory.get_instance("appointment") #AppointmentService()
    vehicle_service =dealer_factory.get_instance("vehicle") #VehicleService()
    dealership = dealer_factory.get_instance("dealership")
    notificationservice = dealer_factory.get_instance("notification")
    """flow for unauthenticated user """
    if request.method == 'POST':
            """here we try to save the user and attach apppointment information with the user """
            dt = request.POST.get("slab_time")
            phone_number = request.POST.get("phone_number_1")
            email = request.POST.get("email_1")
            profile = uservice.get_user_profile_by_phone(phone_number)
            
            if profile ==None:
                    profile = uservice.get_user_profile_by_email(email)
                    print profile
            if profile ==None:
                    profile = UserProfile()
                    
            customer_form = GuestccountForm(request.POST,instance = profile)
            if customer_form.is_valid():
                customer_form.save()
                way_away = request.POST.get("way_away")
                slab_time = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M')
                slab_time = timezone.make_aware(slab_time)
                contact_me = request.POST.get("contact_me")
                email_copy = request.POST.get("email_copy")
                
                comments = request.POST.get("comments")
                app = appt_service.save_appoitment_with(slab_time,None,way_away,None,comments,contact_me,dealer_id=dealer.id)
                if email_copy:
                    appt_service.email_appointment(app)
                appt_service.save_profile(app,profile)
                appt_service.book_appointment(app,dealer=dealer,comments=request.POST.get('comments',''))
                url ="?dealer_code="+dealer_code\
                                            +"&appointment_id="+str(app.id)
                return HttpResponseRedirect(reverse("customer:book_appointment")+url)
            else:
                profile = None  
    else:
            customer_form = GuestccountForm()
    context = {"selected_type":"new_customer",
               "tab":"appointmentnow",
               "dealer_code":dealer_code,
               "way_away":way_away,"customer_form":customer_form
                }
    userservice.set_centrifuge_context(request,dealer_code,None, context)
    return render(request, "customer/book_appointment_now.html",context)

@dealership_required
def save_appointment_now_ext(request,dealer_code):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    dealer = dealer_service.get_dealer_by(dealer_code)
    userservice = customer_factory.get_instance("user")
    appointmentservice = dealer_factory.get_instance("appointment")
    dt = request.GET.get("slab_time")
    advisor = request.GET.get("advisor")
    way_away = request.GET.get("way_away")
    profile_id = request.GET.get("profile_id")
    slab_time = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M')
    slab_time = timezone.make_aware(slab_time)
    contact_me = request.GET.get("contact_me")
    email_copy = request.GET.get("email_copy")
    comments = request.GET.get("comments")
    app = appointmentservice.save_appoitment_with(slab_time,advisor,way_away,profile_id,comments,contact_me,dealer_id=dealer.id)
    if app:
        appointmentservice.book_appointment(app,dealer=dealer)
        if email_copy:
            appointmentservice.email_appointment(app)
        url ="?dealer_code="+dealer_code\
                                            +"&appointment_id="+str(app.id)
        return JsonResponse({"success":True,
                             "msg":"Saved Successfully",
                             "appointment":app.id,
                             "redirect":reverse("customer:book_appointment")+url,
                             },safe=False)
    else:
        return JsonResponse({"success":False,"msg":"Unable to Save"},safe=False)
   
    
@dealership_required
def book_appointment_now_existing(request,dealer_code):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    dealer = dealer_service.get_dealer_by(dealer_code)
    userservice = customer_factory.get_instance("user")
    way_away_service = dealer_factory.get_instance("wayaway")
    way_away = way_away_service.get_all_wayaway(dealer)
    context = {"selected_type":"existing_customer",
               "tab":"appointmentnow",
               "dealer_code":dealer_code,
               "way_away":way_away
                }
    userservice.set_centrifuge_context(request,dealer_code,None, context)
    return render(request, "customer/book_appointment_now.html",context)


def check_userprofile(request):
    customer_factory = CustomerServicesFactory()
    userservice = customer_factory.get_instance("user")
    if request.GET.get("phone_number"):
        phone_number = request.GET.get("phone_number")
        if phone_number:
            phone_number = phone_number.replace("-","")
            profile = userservice.get_user_profile_by_phone(phone_number)
            if profile ==None:
                return JsonResponse({"success":False,"msg":"Phone number doesnt exist"},safe=False)
            else:
                return JsonResponse({"success":True,"msg":"Phone Exists","profile_id":profile.id},safe=False)
        else:
            return JsonResponse({"success":False,"msg":"Phone number doesnt exist"},safe=False)
    else:
        return JsonResponse({"success":False,"msg":"Phone number doesnt exist"},safe=False)



@dealership_required
def get_available_slabs_for_date(request,dealer_code):
    
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    dealer = dealer_service.get_dealer_by(dealer_code)
    dt = request.GET.get("date")
    advisor = request.GET.get("advisor")
    capacity_service = dealer_factory.get_instance("capacity")
     
    if dt:
        slab_date = datetime.datetime.strptime(dt, '%Y-%m-%d')
        slab_date = timezone.make_aware(slab_date)
        slabs = capacity_service.get_available_slabs_for(slab_date,dealer,advisor) 
        return JsonResponse({"success":True,"slabs":slabs},safe=False)
    else:
        return JsonResponse({"success":False,"msg":"Please provide a valid date"},safe=False)
    
@dealership_required
def get_available_adivsors_for_date(request,dealer_code):
    
    dealer_factory = DealerShipServicesFactory()
    customer_factory = CustomerServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    dealer = dealer_service.get_dealer_by(dealer_code)
    dt = request.GET.get("slab_time")
    
    capacity_service = dealer_factory.get_instance("capacity")
    user_service = customer_factory.get_instance("user")
    if dt:
        slab_date = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M')
        slab_date = timezone.make_aware(slab_date)
        advisors = user_service.get_all_available_advisor_for_slab_time(dealer_code,slab_date) 
        return JsonResponse({"success":True,"advisors":advisors},safe=False)
    else:
        return JsonResponse({"success":False,"msg":"Please provide a valid time"},safe=False)
    
@appointment_required
@dealership_required_or_logged_in
def sendemail(request,dealer_code,profile,appointment):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    userservice = customer_factory.get_instance("user")#CUserService()
    notificationservice = dealer_factory.get_instance("notification")
    dealer = dealer_service.get_dealer_by(dealer_code)
    template = "email/appointment_comment.html"
    template_text = "email/appointment_comment.html"
    if request.GET.get("send_email") or  request.GET.get("call"):
        advisor_id = request.GET.get("advisor")
        if advisor_id!="":
            advisor = userservice.get_user_profile(advisor_id)
        if advisor==None:
            advisor = dealership.default_advisor
        send_email = request.GET.get("send_email")
        call =     request.GET.get("call")
        phone_number = request.GET.get("phone_number")

        comment = request.GET.get("comment")
        context = {'comment' : comment , 'advisor':advisor}
        if call  == "true":
            context['phoneno'] = phone_number
        notificationservice.send_notification(advisor,settings.EMAIL_HOST_USER,template,template_text,
                                                  "Customer Comment",context,send_text=False)
        return JsonResponse({"success":True,"send_email":send_email,"call":call,
                             "phone_number":phone_number,"comment":"comment"},safe=False) 

         
    

@appointment_required
@dealership_required_or_logged_in
def book_appointment(request,dealer_code,profile,appointment):
    """
           This is the Book Appointment section
    """
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    uservice = customer_factory.get_instance("user") #CUserService()
    appt_service = dealer_factory.get_instance("appointment") #AppointmentService()
    vehicle_service =dealer_factory.get_instance("vehicle") #VehicleService()
    dealership = dealer_factory.get_instance("dealership")
    notificationservice = dealer_factory.get_instance("notification")
    dealer = dealership.get_dealer_by(dealer_code)
    profile = appointment.customer
    logged_in = False
    customer_form = None
    initial_user_form = None
    usercreateform = None
    if request.user.is_authenticated() and request.user.groups.filter(name__in=[confg.GROUP_NAME]):
            """for authenticated user"""
            profile = request.user.userprofile#uservice.get_user_profile(request.user.id)
            logged_in= True
            if request.method == 'POST':
                appt_service.book_appointment(appointment,dealer=dealer)
            appt_service.save_profile(appointment,profile)#atttching the profile to appointment
            vehicle_service.save_vehicle_for(profile,appointment.vehicle)#attacging the vehicle to the profile
    else:
        """flow for unauthenticated user """
        if request.method == 'POST':
            """here we try to save the user and attach apppointment information with the user """
            
            phone_number = request.POST.get("phone_number_1")
            email = request.POST.get("email_1")
            profile = uservice.get_user_profile_by_phone(phone_number)
            if profile ==None:
                    profile = uservice.get_user_profile_by_email(email)
            if profile ==None:
                    profile = UserProfile()
                
            customer_form = GuestccountForm(request.POST,instance = profile)
            if customer_form.is_valid():
                customer_form.save()
                if request.POST.get("contact_me_appointment"):
                    appt_service.contact_me(appointment,request.POST.get("contact_me_time"))
                    
                if request.POST.get("reminder_settings"):
                    emailset=False
                    textset=False
                    phoneset = False
                    if request.POST.get("setting_email"):
                        emailset = True
                    if request.POST.get("setting_text"):
                        textset=True
                    if request.POST.get("setting_phone"):
                        phoneset=True
                    reminder = notificationservice.create_reminder_setting_for(notificationservice.SCHEDULE_APPOINTMENT_TYPE,profile)
                    notificationservice.save_reminder_settings(reminder.id,emailset,textset,phoneset)
                    
                appt_service.save_profile(appointment,profile)
                vehicle_service.save_vehicle_for(profile,appointment.vehicle)
                appt_service.book_appointment(appointment,dealer=dealer,comments=request.POST.get('comments',''))
            else:
                
                profile = None  
        else:
            customer_form = GuestccountForm()
            
        if profile:
            initial_user_form = {"profile":profile.id}
            usercreateform = CreateUserForm(initial = initial_user_form)
            
            
    isbooked = appt_service.isbooked(appointment)        
    tab= "book"
    print logged_in
    context = {"page_title":"Book appointment","services_list":appointment.appointmentservice.all(),
                                          "appointment":appointment,
                                          "dealer_code":dealer_code
                                          ,"tab":tab,
                                          "profile":profile,
                                          "logged_in":logged_in,
                                          "customer_form":customer_form,
                                          "isbooked":isbooked,
                                          "dealer":dealer,"GOOGLE_KEY":settings.MAP_KEY,
                                          "usercreationform": usercreateform,"request":request,"services":appointment.appointmentservice
                }
    uservice.set_centrifuge_context(request,dealer_code,profile, context,chatposition="top")
    return render(request, "customer/appointment/book_appointment.html",context)



@dealership_required
def search_app(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealership_service = dealer_factory.get_instance("dealership")
    dealer = dealership_service.get_dealer_by(dealer_code)
    service = dealer_factory.get_instance("appointment")
    code = None
    vin_number = None
    liscense_number = None
    make  = None
    model = None
    if  dealer:
        if request.GET.get("confirmation_phone") :
            code = request.GET.get("confirmation_phone")
            code = code.replace("-","")
        if request.GET.get("vin_number") :
            vin_number = request.GET.get("vin_number")
        if request.GET.get("liscense_number") :
            liscense_number = request.GET.get("liscense_number")
            
        if request.GET.get("make") :
            make = request.GET.get("make")
        if request.GET.get("model") :
            model = request.GET.get("model")
            
            
        appointments =  service.find_by_confirmation_phone(dealer,code=code,liscense_number=liscense_number,vin_number=vin_number,make=make,model=model)

        
        if appointments:
            return render(request,
                           "customer/partials/search_appointments.html",
                           {"appointments":appointments,"dealer_code":dealer_code
                                          })
        else:
            raise Http404("No vehicle found")



@dealership_required
def find_exiting_appointment(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    service = dealer_factory.get_instance("vehicle")#VehicleService
    dealer_service = dealer_factory.get_instance("dealership")
    if request.user.is_authenticated() and request.user.groups.filter(name__in=[confg.GROUP_NAME]):
            return HttpResponseRedirect(reverse('customer:main'))
        
    dealership = dealer_service.get_dealer_by(dealer_code)
    userservice = customer_factory.get_instance("user")#CUserService()
    loginform = LoginForm()
    vinmg = UploadVinForm() 
    #vehichles = service.get_vehichles()
    vehichles = service.get_vehichles_dealer(dealership)
    vehicles = list(vehichles)
    context = {
                'acitve' : True,
                "dealer_code":dealer_code,
                "bmw_make_settings":settings.BMW_MAKE_CODE,
                "tab":"find","loginform":loginform,"vinmg":vinmg, "vehicles":mainjson.dumps(vehicles),}
    userservice.set_centrifuge_context(request, dealer_code,None,context)
    template_name = 'customer/find_app.html'
    return render(request, template_name, context)


@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)   
@dealership_required_or_logged_in  
def schedule_appointment(request,dealer_code,profile):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    service_layer = customer_factory.get_instance("user")#CUserService()
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    if request.GET.get("customer_vehicle_id"):
        vehicle_id = request.GET.get("customer_vehicle_id")
        appt_service = dealer_factory.get_instance("appointment")#AppointmentService()
        appt = appt_service.save_empty_appointment(dealer_id=dealership.id)
        appt.vehicle_id = vehicle_id
        if profile:
            appt.customer_id = profile.id
            myadvisor = service_layer.get_my_advisor(profile.id,dealership.id)
            if myadvisor:
                appt.advisor = myadvisor
        appt.save()
        url ="?appointment_id="+str(appt.id)
        return HttpResponseRedirect(reverse("customer:service_selection_appointment")+url)
    
    
    
# @user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)
@dealership_required_or_logged_in
def cancel_appointment(request,dealer_code,profile):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.GET.get("appointment_id"):
        try:
            appointment_id = request.GET.get("appointment_id")
            appt_service = dealer_factory.get_instance("appointment")
            appt_service.cancel_appointment(appointment_id)
            referer =request.GET.get("referer") 
            messages.success(request, "Your Appointment has been Cancelled")
            if referer:
                return HttpResponseRedirect(referer)
            else:
                return HttpResponseRedirect(reverse("customer:main"))
        except:
            raise Http404("No vehicle found")
    else:
        raise Http404("No Appointment found")
        
        
@dealership_required_or_logged_in
def search_by_code_phone(request,dealer_code,profile):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    service = dealer_factory.get_instance("vehicle")#VehicleService()
    dservice = dealer_factory.get_instance("dealership")#DealerShipService()
    appointmentservice = dealer_factory.get_instance("appointment")
    dealer = dservice.get_dealer_by(dealer_code)
    appointments = None
    appointment = None
    if request.GET.get("code") or request.POST.get("code"):
        code = request.GET.get('code')
        if code ==None:
            code = request.POST.get('code')
        appointments = appointmentservice.get_appointments_by_phone(dealer,code)
        if len(appointments) ==0:
            appointments =appointmentservice.get_appointmets_by_confirmation(dealer,code)
    else:
        if profile:
            appointments = appointmentservice.get_appointmets_by_profile(dealer,profile)
            
    services_list = None    
    if request.GET.get("appointment_id") !=None:
        appointment = appointmentservice.get_active_appointment(request.GET.get("appointment_id"))        
        try:
            services_list = appointment.appointmentservice.all()
            
        except Exception,e:
#             print e
            services_list = None
#         print services_list
    context = {"page_title":"Appointments",
                                          "dealer_code":dealer_code,
                                          "appointments":appointments,
                                          "request":request,
                                          "appointment":appointment,
                                        "services_list":services_list
                                          }
    
    return render(request, "customer/appointment/search_phone_confirmation.html",context)
 
@appointment_required
@dealership_required_or_logged_in
def date_selection_appointment(request,dealer_code,profile,appointment):
    """
           This is the Date selection for an appointment
    """
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    tab= "appointment"
    userservice = customer_factory.get_instance("user")#CUserService()  
    accordion = request.GET.get("accordion","advisor")
   
    context = {"page_title":"Select Service and Repair",
                                          "appointment":appointment,"dealer_code":dealer_code
                                          ,"tab":tab,"services_list":appointment.appointmentservice.all(),"accordion":accordion
                                          }
    userservice.set_centrifuge_context(request,dealer_code,profile, context,chatposition="top")
    return render(request, "customer/appointment/date_advisor_selection.html",context)

@appointment_required
@dealership_required_or_logged_in
def service_selection_appointment(request,dealer_code,profile,appointment):
    """
           This is the service and repair selection screen
    """
    tab= "service"
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    userservice = customer_factory.get_instance("user")#CUserService()
    profile = None  
    myadvisor  = None
    all_advisors = None
    if appointment.customer:
        profile =  appointment.customer
        myadvisor = userservice.get_my_advisor(profile.id,dealership.id)
    accordion = request.GET.get("accordion","services")
    all_advisors = userservice.get_all_advisor_for(dealer_code)
    context = {"page_title":"Select Service and Repair", "dealer_code":dealer_code,
                                          "appointment":appointment,"tab":tab,
                                         "all_advisors":all_advisors,
                                         "myadvisor":myadvisor,"profile":profile,
                                          "services_list":appointment.appointmentservice.all(),
                                          "accordion":accordion
                                          }
    userservice.set_centrifuge_context(request,dealer_code,profile, context,chatposition="top")
    return render(request, "customer/appointment/service_selection.html",context)
   

@appointment_required
@dealership_required_or_logged_in
def vehicle_selection(request,dealer_code,profile,appointment):
    """
            this is the vehicle selection screen for the appointment
    """
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    service = dealer_factory.get_instance("vehicle")#VehicleService()
    userservice = customer_factory.get_instance("user")#CUserService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code"))
    name= ""
    tab= ""
  
    instance = None
    milage = None
            
    if  appointment.vehicle:        
        make = appointment.vehicle.vehicle.make.id
        year =  appointment.vehicle.vehicle.year.id  
        vin_number = appointment.vehicle.vin_number
        milage = appointment.vehicle.milage
        
    else:
        make = request.GET.get(confg.SESSION_MAKE_KEY,"") 
        year =  request.GET.get(confg.SESSION_YEAR_KEY,"")  
        vin_number = request.GET.get(confg.SESSION_VIN_NUM_KEY,"")
     
    
    vehichles = service.get_vehichles_dealer(dealership)
    vehicles = list(vehichles)
    media_url = settings.MEDIA_URL
    tab = ""
    if request.method == 'POST':
        vehicle_form = CustomerVehichleForm(request.POST,
                                            instance=appointment.vehicle)
        if vehicle_form.is_valid():
            try:
                customer_vehicle =  vehicle_form.save()
                appointment.vehicle=  customer_vehicle#service.get_customer_vehicle(customer_vehicle.pk)
                appointment.save()
                service.save_vehicle_vin_data(customer_vehicle,request.POST.get("vin_data"))
                messages.success(request, "You have selected you vehicle. Please select services and repairs")
                url ="?dealer_code="+dealer_code\
                                            +"&appointment_id="+str(appointment.id)
               
                return HttpResponseRedirect(reverse("customer:service_selection_appointment")+url)
            except Exception,e:
                vehicle_form.add_error(None,"Some error occured while saving"+str(e))
    else:
        
        vehicle_form = CustomerVehichleForm(initial={'user': profile,
                                                     "vin_number":vin_number,
                                                     "milage":milage},instance=appointment.vehicle)
    accordion = request.GET.get("accordion","main")
    if appointment.vehicle:
        accordion = "model"
    context = {"page_title":"Select Model",
                                          "media_url":media_url,'name':name,
                                          "vehicles":mainjson.dumps(vehicles),
                                          "tab":tab,
                                          'acitve' : True,
                                          "make":make,"year":year,
                                          "vin_number":vin_number,"media_url":media_url,
                                          "vehicle_form":vehicle_form,
                                          "dealer_code":dealer_code,
                                          "appointment":appointment,
                                          "accordion":accordion
                                          
                                          }
    userservice.set_centrifuge_context(request,dealer_code,profile, context,chatposition="top")
    return render(request, "customer/appointment/vehicle_selection.html",context)
   
        

