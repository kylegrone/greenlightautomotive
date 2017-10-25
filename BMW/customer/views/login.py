# Create your views here.
'''Login for Customers'''

from datetime import date, timedelta
import json
import os

from django.conf import settings
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, request
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.timezone import get_current_timezone
from googleapiclient import discovery
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_orm import Storage

from BMW import settings
from apiclient.discovery import build
from customer.app_confg import confg
from customer.decorators.decorators import customer_group_check, dealership_required
from customer.factories import CustomerServicesFactory
from customer.forms import CustomerVehichleForm, ImageUploadForm
# from customer.models import CredentialsModel, FlowModel
from customer.services.google import GoogleService
from customer.services.importservice import ImportContact
from customer.services.userservices import CUserService
from dealership.factories import DealerShipServicesFactory
from dealership.forms import *
from dealership.models import VinYear
import json as mainjson
from livechat.forms import UploadForm
from livechat.models import Upload
from string import lower


def auth_return(request):
#     user = request.user
    if request.session.get("oauth_appointment"):
        customer_factory = CustomerServicesFactory()
        dealer_factory = DealerShipServicesFactory()
        dealer_service = dealer_factory.get_instance("dealership")
        appt_service = dealer_factory.get_instance("appointment") #AppointmentService()
        appointment  =appt_service.get_appointment(request.session.get("oauth_appointment"))#,dealer)
#         if not xsrfutil.validate_token(
#                 settings.SECRET_KEY, request.REQUEST['state'], user):
#             return HttpResponseBadRequest()
        FLOW = FlowModel.objects.get(id=appointment).flow
        credential = FLOW.step2_exchange(request.REQUEST)
        storage = Storage(CredentialsModel, 'id', appointment, 'credential')
        storage.put(credential)
        return HttpResponseRedirect(reverse('customer:sync_gcalendar')+"?appointment_id="+str(appointment.id))
    



def import_csv(request):
    imprt = ImportContact()
    row = [""] * 100 
    row[1] = "test"
    row[2] = "user"
    row[3] = "test.user@gmail.com"
    row[4] = "(1231)1231-1231"
    row[5] = "(1231)1231-1231"
    
    row[6] = "US"
    row[7] = "House # 4151 st #10"
    row[8] = " California"
    row[9] = "CA"
    row[10] = "1231"
    row[18] = "2007"
    row[19] = "Infiniti"
    row[20] = "Q3"
    row[26] = "123131"
    row[28] = "Black"
    row[29] = 1110
    row[33] = "11/04/2015 01:16 PM"
    row[34] = "11/04/2015 01:16 PM"
    row[35] = "Rachel Blach"
    row[41] = "Oil change"
    row[44] = 100
    row[45] = "completed"
#     imprt.add_row(row)
    imprt.import_file()
    
    
def sync_gcalendar(request):
    gcalservice = GoogleService()
    if request.GET.get("appointment_id"):
        if request.GET.get("refferrer"):
            request.session["refferrer"] =request.GET.get("refferrer") 
        
        customer_factory = CustomerServicesFactory()
        dealer_factory = DealerShipServicesFactory()
        dealer_service = dealer_factory.get_instance("dealership")
#         dealer = dealer_service.get_dealer_by(dealer_code)
        uservice = customer_factory.get_instance("user") #CUserService()
        appt_service = dealer_factory.get_instance("appointment") #AppointmentService()
        appointment  =appt_service.get_appointment(request.GET.get("appointment_id"))#,dealer)

#         REDIRECT_URI = 'http://127.0.0.1:8000/customer/oauth2callback/'#?appointment_id='+request.GET.get("appointment_id")
        request.session["oauth_appointment"]  =request.GET.get("appointment_id")
        #REDIRECT_URI = "https://%s%s" % (
        #   get_current_site(request).domain, reverse("customer:return"))
        REDIRECT_URI = settings.SITE_MAIN_URL+reverse("customer:return")
        CLIENT_SECRETS = os.path.join(
        os.path.dirname(__file__), gcalservice.CLIENT_SECRET_FILE)
        
        FLOW = flow_from_clientsecrets(
            CLIENT_SECRETS,
            scope=gcalservice.SCOPES,
            redirect_uri=REDIRECT_URI
        )
        storage = Storage(CredentialsModel, 'id', appointment, 'credential')
        credential = storage.get()
        if credential is None or credential.invalid is True:
            FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY, appointment)
            authorize_url = FLOW.step1_get_authorize_url()
            f = FlowModel(id=appointment, flow=FLOW)
            f.save()
            
            return HttpResponseRedirect(authorize_url)
        else:
            resp = gcalservice.create_event(appointment,credential)
            messages.success(request, "Your appointment has been added to Google Calendars")
            if request.session.get("refferrer"):
                refferrer =request.session["refferrer"]
                del request.session["refferrer"]
                return HttpResponseRedirect(refferrer)
            else:
            
                return JsonResponse({"success":resp},safe=False) 
            
            
@dealership_required
def testing(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code")) 
    capacityservice = dealer_factory.get_instance("capacity")
#     slab_time = timezone.now() - timedelta(hours=44)
    slab_time = datetime.datetime.strptime('Jan 29 2016  9:20AM', '%b %d %Y %I:%M%p')
    slab_time = timezone.make_aware(slab_time)
    print slab_time
    capacity = capacityservice.check_slab_availibity(slab_time,dealership)
    print capacity
#   


def pull_models(request):
    dealer_id = 1
    year = 2017
    models = ["230i Convertible","230i Coupe","230i xDrive Convertible","230i xDrive Coupe","320i Sedan","320i xDrive Sedan","328d Sedan","328d xDrive Sedan","328d xDrive Wagon","330e iPerformance","330i Sedan","330i xDrive Gran Turismo","330i xDrive Sedan","330i xDrive Wagon","340i Sedan","340i xDrive Gran Turismo","340i xDrive Sedan","430i Convertible","430i Coupe","430i Gran Coupe","430i xDrive Convertible","430i xDrive Coupe","430i xDrive Gran Coupe","440i Convertible","440i Coupe","440i Gran Coupe","440i xDrive Convertible","440i xDrive Coupe","440i xDrive Gran Coupe","530i Sedan","530i xDrive Sedan","535i Gran Turismo","535i xDrive Gran Turismo","540i Sedan","540i xDrive Sedan","550i xDrive Gran Turismo","640i Convertible","640i Coupe","640i Gran Coupe","640i xDrive Convertible","640i xDrive Coupe","640i xDrive Gran Coupe","740i Sedan","740i xDrive Sedan","750i Sedan","750i xDrive Sedan","ALPINA B6 xDrive Gran Coupe","ALPINA B7 xDrive","M2","M240i Convertible","M240i Coupe","M240i xDrive Convertible","M240i xDrive Coupe","M3 Sedan","M4 Convertible","M4 Coupe","M6 Convertible","M6 Coupe","M6 Gran Coupe","M760i xDrive Sedan","X1 sDrive28i","X1 xDrive28i","X3 sDrive28i","X3 xDrive28d","X3 xDrive28i","X3 xDrive35i","X4 M40i","X4 xDrive28i","X5 M","X5 sDrive35i","X5 xDrive35i","X5 xDrive40e","X5 xDrive50i","X6 M","X6 sDrive35i","X6 xDrive35i","X6 xDrive50i","i3","i3 (60 ah)","i3 with Range Extender","i8"]
    make_id = 2
    for model in models:
        try:
            m = VinModel.objects.get(name=model)
        except Exception,e:
            m = VinModel(name=model,val=model)
            m.save()
        try:
            y = VinYear.objects.get(name=year)
        except Exception,e:
            y = VinYear(name=year,val=year)
            y.save()
        try:
            vehicle = Vehicle.objects.get(model=m,year=y,make_id=make_id)
        except Exception,e:
            vehicle = Vehicle(model=m,year=y,make_id=make_id)
            vehicle.mainimage = model.lower()+".jpg"
            vehicle.save()
#         image = get_image(model,year)
#         if image:
#             vehicle.mainimage = 
        try:
            dealer_vehicle = DealersVehicle.objects.get(vehicle=vehicle,dealer_id=dealer_id)
        except Exception,e:
            dealer_vehicle = DealersVehicle(vehicle=vehicle,dealer_id=dealer_id)
            dealer_vehicle.save()
    return JsonResponse({"success":True},safe=False) 
def get_image(model,year):
    url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAbVHjVJZHFh6jQZkh1XkhQ-e-gCTQ1rOA&cx=009864217067913918543:rlma41jwnds&q="+model+" "+year
    js = json.loads(url)




@dealership_required  
def delete_models(request,dealer_code=None):
  
            
    if dealer_code:
        year = 1998
        if request.GET.get("year")!=None:
            year = request.GET.get("year")
           
        if request.POST.get("models")!=None:
            models = request.POST.getlist("models")
#             delete_vehicle = DealersVehicle.objects.filter(vehicle__year__name = year)
            delete_vehicle = DealersVehicle.objects.filter(id__in=models)
            delete_vehicle.delete()
        dealer = Dealer.objects.get(dealer_code=dealer_code)
        dvs = DealersVehicle.objects.filter(dealer_id = dealer.id).order_by("vehicle__model__name")
        
        
        dvs = dvs.filter(vehicle__year__name=year)
        
        return render(request, "customer/delete_models.html",
                          {"dealer_code":dealer_code,
                           "dvs":dvs,"year":year
                           })
        
@dealership_required  
def create_models(request,dealer_code=None):
    
            
    if dealer_code:
        dealer = Dealer.objects.get(dealer_code=dealer_code)
        if request.POST.get("make")!=None:
            make_c = request.POST.get("make")
            year_c = request.POST.getlist("year")
            model_text = request.POST.get("model_text")
            model_c = request.POST.get("model")
            form = ImageUploadForm(request.POST, request.FILES)
            pic = None
            if form.is_valid():
                print "form is valid"
                pic =  form.cleaned_data['image']
                print pic
            else:
                print "form is not valid"
            if model_text!=None and model_text.strip!="":
                try:
                    tmpmodel = VinModel.objects.get(name=model_text.strip())
                except Exception,e:
                    model_obj  = VinModel(name=model_text.strip(),val=model_text.strip())
                    model_obj.save()
                    model_c = model_obj.id
            
                
            if make_c and model_c and year_c:
                for year_id in year_c:
                    try:
                        vehicle = Vehicle.objects.get(make_id=make_c,model_id=model_c,year_id=year_id)
                    except Exception,e:
                        vehicle = Vehicle(make_id=make_c,model_id=model_c,year_id=year_id)
                        if pic:
                            vehicle.mainimage = pic
                        vehicle.save()
                    try:
                        DealersVehicle.objects.get(dealer_id=dealer.id,vehicle=vehicle)
                    except Exception,e:
                        dtmp = DealersVehicle(dealer_id=dealer.id,vehicle=vehicle)
                        dtmp.save()
                        
        make = VinMake.objects.all().order_by("name")
        year = VinYear.objects.all().order_by("name")
        model = VinModel.objects.all().order_by("name")
        return render(request, "customer/create_models.html",
                          {"dealer_code":dealer_code,
                           "make":make,"year":year,"model":model
                           })
@dealership_required
def registeruer(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    cuser = customer_factory.get_instance("user")
    if request.GET.get("profile_id"):
        profile = cuser.get_user_profile( request.GET.get("profile_id"))
        if profile:
            initial_user_form = {"profile":profile.id}
            usercreateform = CreateUserForm(initial = initial_user_form)
            return render(request, "customer/registeruser.html",
                          {"usercreationform":usercreateform,"profile":profile,
                           "done_disable":True,"request":request})
        else:
            raise Http404("Profile not found")


@dealership_required
def createuser(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    userservice = customer_factory.get_instance("user")#CUserService()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)        
        if form.is_valid():
            username = form.cleaned_data['username']
            profile_id = form.cleaned_data["profile"]
            profile =userservice.get_user_profile(profile_id)
            user = userservice.create_customer(username)
            referrer = request.POST.get("referrer")
            if user:
                user.set_password(form.cleaned_data['new'])
                user.save()
                messages.success(request, "Account has been successfully created. Your information will be stored for future service appointment needs. Please click 'DONE' to review your appointment, make changes or cancel the appointment.")
                if profile:
                    profile.user = user 
                    profile.save()
                    if referrer:
                        return HttpResponseRedirect(referrer)
                    else:
                        return HttpResponseRedirect(reverse('customer:index')+"?dealer_code="+dealer_code)
        else:
            print form.errors
            print "form not valid"
#             password = user_service.save_user_password(user, form.cleaned_data['new'])
        
        
        
def check_username(request):
    if request.GET.get("username"):
        username = request.GET.get("username")
        try:
            user = User.objects.get(username=username)
            return JsonResponse({"success":True},safe=False) 
        except:
            return JsonResponse({"success":False},safe=False) 
    

@dealership_required
def new_customer_vehicle(request,dealer_code=None):
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.user.is_authenticated() and request.user.groups.filter(name__in=[confg.GROUP_NAME]):
            return HttpResponseRedirect(reverse('customer:main'))
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(request.session.get("dealer_code")) 
    service = dealer_factory.get_instance("vehicle")#VehicleService()
    userservice = customer_factory.get_instance("user")#CUserService()
#     vehichles = service.get_vehichles()
    vehichles = service.get_vehichles_dealer(dealership)
    appservice  = dealer_factory.get_instance("appointment")#appointmentservices.AppointmentService()
    vehicles = list(vehichles)
    media_url = settings.MEDIA_URL
    customer_vehicle = None
    if request.method == 'POST':
        if request.POST.get("make")!= None and request.POST.get("year")  !=None:
            if request.POST.get("vehicle_id") !=None and request.POST.get("vehicle_id")!="":
                customer_vehicle = service.save_customer_vehicle(None,request.POST.get("vehicle_id"),request.POST.get("vin_vehicle"),request.POST.get("desc_vehicle",""))
            
            app = appservice.save_empty_appointment(dealership.id)
            vehicle_desc = request.POST.get("desc_vehicle","test")
            if app:
                url ="?dealer_code="+dealer_code+"&"+confg.SESSION_MAKE_KEY\
                                                +"="+request.POST.get("make")\
                                                +"&"+confg.SESSION_YEAR_KEY+"="+request.POST.get("year")\
                                                +"&appointment_id="+str(app.id)
                
                if customer_vehicle and customer_vehicle.vehicle :
                    appservice.save_customer_vehicle(app,customer_vehicle.id)
                    if request.POST.get("vin_data")!=None and request.POST.get("vin_data")!="":
                        service.save_vehicle_vin_data(customer_vehicle,request.POST.get("vin_data"))
                    return HttpResponseRedirect( reverse('customer:service_selection_appointment')+url)
                else:
                    if request.POST.get("vin_vehicle") !=None:
                        url+= "&"+confg.SESSION_VIN_NUM_KEY+"="+request.POST.get("vin_vehicle")
                    return HttpResponseRedirect( reverse('customer:vehicle_selection_appointment')+url) 
            else:
                    messages.error(request, 'Unable to save appointment. Please try later') 
 
    
    context = {
                 'acitve' : True,
                "dealer_code":dealer_code,
                "tab":"new",
                "media_url":media_url,
                "vehichles":mainjson.dumps(vehicles),
                "bmw_make_settings":settings.BMW_MAKE_CODE
                }
    userservice.set_centrifuge_context(request,dealer_code,None, context)
    template_name = 'customer/new_user_vehicle.html'
    return render(request, template_name, context)




@dealership_required
def login(request,dealer_code=None):
    '''Get username ,password and authenticate '''
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.user.is_authenticated() and request.user.groups.filter(name__in=[confg.GROUP_NAME]):
            return HttpResponseRedirect(reverse('customer:main'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            
            if user is not None:                
                if user.is_active:
                    auth_login(request, user)
                    request.session["dealer_code"] = dealer_code
                    referrer = request.POST.get("referrer","")
                    if referrer and referrer!="" :
#                         return HttpResponseRedirect(reverse('customer:main'))
                        return HttpResponseRedirect(referrer)
                    else:
                        return HttpResponseRedirect(reverse('customer:main'))
                else:
                    form.add_error("username","User is not active")
            else:
                try:
                    user = User.objects.get(username=form.cleaned_data['username'])
                    form.add_error("username","Password is incorrect.")
                except Exception,e:
                    form.add_error("username","Username is incorrect.")
    else:
        form = LoginForm()
       
    '''Chat Setup'''
    userservice = customer_factory.get_instance("user")
   
    context = {'form':form,
              
                 'acitve' : True,"dealer_code":dealer_code,"tab":"","request":request}
#     userservice.set_centrifuge_context(request,dealer_code,None, context)
    userservice.set_centrifuge_context(request,dealer_code,None, context)
    template_name = 'customer/login_form.html'
    return render(request, template_name, context)


    
    
    

@dealership_required
def index(request,dealer_code=None):
    '''Main Page View'''
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.user.is_authenticated() and request.user.groups.filter(name__in=[confg.GROUP_NAME]):
            return HttpResponseRedirect(reverse('customer:main'))
    form = LoginForm()
    userservice = customer_factory.get_instance("user")#CUserService()
    
    context = {'form':form,"dealer_code":dealer_code,"tab":"","request":request}
    
    template_name = 'customer/login_form.html'
    userservice.set_centrifuge_context(request,dealer_code,None, context)
    return render(request, template_name , context)




@dealership_required
def passreset(request,dealer_code=None):
    '''Reseting Password email'''
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.method == 'POST':
        form = ResetForm(request.POST)        
        if form.is_valid():
            try:
                user_service = customer_factory.get_instance("user")
                profile = user_service.get_user_profile_by_email(form.cleaned_data['email'])
                if profile ==None:
                    raise Exception("Email not found")

                token = user_service.create_token(profile.user)
                try:      
                    user_service.send_pass_reset_link_profile(profile, token,form.cleaned_data['email'],dealer_code)           
                    messages.success(request, 'Email has been sent') 
                                 
                except Exception,e:
                    print e
                    form.add_error("email","email sending failed")
                                 
            except Exception,e: 
                form.add_error("email","email doesnot exist")  
    else:
        form = ResetForm()
    template = 'customer/password_reset.html'
    context= {'form':form,"dealer_code":dealer_code}
    return render(request, template, context)

@dealership_required
def passcreate(request,dealer_code=None):
    '''Setting new password'''
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    form = UserPasswordResetForm()
    template = 'customer/404.html'
    question = ''
    token = request.GET.get('token')
    if token is not None:
        user_service = customer_factory.get_instance("user")
        user = user_service.get_user_from_token(token)
        if user is not None:
            template = 'customer/password_create.html'
#             question =  user_service.get_user_question(user) 
            if request.method == 'POST':
                form = UserPasswordResetForm(request.POST)                   
                if form.is_valid():
#                     if user_service.verify_user_answer(user, form.cleaned_data['answer']) == True:
                        user_service.save_user_password(user, form.cleaned_data['new'])
                        messages.success(request, 'Password has been updated. Please provide the new credentials')
                        return HttpResponseRedirect(reverse('customer:index')+"?dealer_code="+dealer_code)
#                     else:
#                         form.add_error("answer","You have not provided the correct answer")  
                else:
                    print form.errors
            
        else:
            print "user not found"
    
    context ={'form': form, 'question' : None, 'token':token,"dealer_code":dealer_code}
    return render(request, template, context)


def logout(request):
    '''logout view '''
    url = reverse('customer:index')+"?dealer_code="+request.session["dealer_code"]
    auth_logout(request)
    return HttpResponseRedirect(url) 


@dealership_required
def userreset(request,dealer_code=None):
    '''Forgot Username Email'''
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    if request.method == 'POST':
        form = ResetForm(request.POST)        
        if form.is_valid():
            try:
                user_service = customer_factory.get_instance("user")
                profile = user_service.get_user_profile_by_email(form.cleaned_data['email'])
                if profile == None:
                    raise Exception("Email not found")
                try:      
                    user_service.send_username_link_profile(profile.user,form.cleaned_data['email'])           
                    messages.success(request, 'Email has been sent')                 
                except Exception,e:
                    print e
                    form.add_error("email","email sending failed")                 
            except Exception,e:
                print e
                form.add_error("email","email doesnot exist")  
    else:
        form = ResetForm()
    template = 'customer/username_reset.html'
    return render(request, template, {'form': form,"dealer_code":dealer_code})