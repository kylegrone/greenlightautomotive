import datetime
import json

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User , Group
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

from customer.factories import CustomerServicesFactory
from customer.forms import ImageUploadForm
from dealership import conf
from dealership.decorators import *
from dealership.decorators import dealer_group_check
from dealership.factories import DealerShipServicesFactory
from dealership.forms import *
from dealership.managedealershipform import DetailForm , BmwResourceForm , NewUserAdvisorForm , PackageForm, CategoryForm , ItemForm, NewFlagForm
from dealership.services.appointmentservices import AppointmentService
from dealership.services.breadcrumb import BreadCrumb
from dealership.services.managedealer import ManageDealer


@onlydealer_access_check
def manage(request):
    dealer_factory = DealerShipServicesFactory() 
    dealer_session_id = request.session.get("dealer_id")
    md = ManageDealer()
    data = md.getdetail(dealer_session_id)
    breadcrumb = BreadCrumb()
    breadcrumb = breadcrumb.create_breadcrumb(["manage"])
    template = 'manage/index.html'
    qstring = {}
    dform = DetailForm(instance = data)
    amenities = Amenities.objects.all()
    dealer_amenities = md.getamenities(dealer_session_id)
    adv_users = UserProfile.objects.filter(user__groups__id = 4 , dealer_id =request.session.get("dealer_id"))
    app_users = UserProfile.objects.filter(dealer_id = dealer_session_id).exclude(user__groups__id=4) 
    teamslist = Team.objects.filter(created_by_id = dealer_session_id)
    brform = BmwResourceForm()
    pform = PackageForm()
    catform = CategoryForm()
    iform = ItemForm()
    nfform = NewFlagForm()
    for key, value in request.GET.iteritems():
        qstring[key] = value
    packages = InspectionPackage.objects.filter(dealer_id =request.session.get("dealer_id"))
    dealer_service = dealer_factory.get_instance("dealership")
    favorites = dealer_service.get_dealer_favorites(request.session["dealer_id"])
    flag_types = Flags.objects.filter(dealer_id=request.session["dealer_id"]).values('type').order_by('type').distinct()
    flag_data = []
    items_all = InspectionItems.objects.all()
    for obj in flag_types:
        fdic={}
        fdic["type"] = obj["type"]
        fdic["data"] = md.get_flag_data_bydealer(obj["type"],request.session["dealer_id"])
        flag_data.append(fdic)
    config = {"username":request.user,
              "dealer_code":request.session["dealer_code"],
              "dealer_name":request.session["dealer_name"],
              "dealer_id":request.session["dealer_id"],
              "group":request.session["group"],
              "tab":"manage",
              "CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
              "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET}

    context = {'config':config,
               "favorites":favorites,
               'breadcrumb':breadcrumb,
               'qstring':qstring , 
               'dform':dform , 
               'aform':amenities , 
               'brform':brform , 
               'damenities' : dealer_amenities ,
               'advs' : adv_users , 
               'app_users' : app_users , 
               'teaml':teamslist,
               'packages':packages,
               'pform':pform,
               'catform':catform,
               'iform': iform,
               "flags": flag_data,
               'nfform':nfform,
               'items_all':items_all}

    return render(request, template, context)
    


@onlydealer_access_check 
def delete_models(request):
  
    dealer_code = request.session.get("dealer_code")      
    if dealer_code:
        year = 1998
        years = VinYear.objects.all()
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
        
        return render(request, "dealership/delete_models.html",
                          {
                           "dvs":dvs,"year":str(year),
                           "years":years,
                           "dealer_code":request.session["dealer_code"],
                           "config":{
                                     "username":request.user,
                           "dealer_code":request.session["dealer_code"],
                
                            "dealer_name":request.session["dealer_name"],
                            "dealer_id":request.session["dealer_id"]}  
                           })
        
@onlydealer_access_check
def create_models(request):
    
    dealer_code = request.session.get("dealer_code")           
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
        return render(request, "dealership/create_models.html",
                          {"dealer_code":request.session["dealer_code"],
                            "dealer_code":request.session["dealer_code"],
                            "config":{
                                      "username":request.user,
                           "dealer_code":request.session["dealer_code"],
                
                            "dealer_name":request.session["dealer_name"],
                            "dealer_id":request.session["dealer_id"]},
                           "make":make,"year":year,"model":model
                           })

    
@csrf_exempt    
def details(request):
    template = 'manage/details.html'
    md = ManageDealer()
    data = md.getdetail(request.session.get("dealer_id"))
    if request.method == "POST":
        form = DetailForm(request.POST , request.FILES , instance = data)
        if form.is_valid():
            form.save()
        else:
            print form.errors
                 
    dform = DetailForm(instance = data)   
    return render(request,template,{'dform':dform})
     
@csrf_exempt  
def add_amenities(request):
    template = 'manage/amenities.html'
    if request.method == "POST":
        print request.POST['id']
        amn = ShopAmenities(amenities_id = request.POST['id'] , shop_id = request.session.get("dealer_id"))
        amn.save()
    return render(request , template)

@csrf_exempt 
def delete_amenities(request):
    template = 'manage/amenities.html'
    if request.method == "POST":
        print request.POST['id']
        ShopAmenities.objects.get(amenities_id = request.POST['id'] , shop_id = request.session.get("dealer_id")).delete()
    return render(request , template)

def get_resource_link(request):
    data_arr = []
    if request.method == "GET":
        data = BMWResourceLink.objects.filter(shop_id = request.session.get("dealer_id"))
        for obj in data:
            data_dic = {}
            data_dic['id'] = obj.id
            data_dic['Name'] = obj.name
            data_dic['Rank'] = obj.rank
            data_dic['URL'] = obj.url
            data_arr.append(data_dic)
    return HttpResponse(json.dumps(data_arr))
@csrf_exempt
def add_resource_link(request):
    if request.method == "POST":
        brl = BMWResourceLink(name = request.POST['Name'] , url = request.POST['URL'] , rank = request.POST['Rank'] , shop_id =  request.session.get("dealer_id"))
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Added Successfully'}))

@csrf_exempt
def delete_resource_link(request):
    if request.method == "POST":
        BMWResourceLink.objects.get(id= request.POST['id']).delete()
       
    return HttpResponse(json.dumps({'message' : 'Deleted Successfully'}))
@csrf_exempt
def update_resource_link(request):
    if request.method == "POST":
        brl = BMWResourceLink.objects.get(id= request.POST['id'])
        brl.name = request.POST['Name']
        brl.url = request.POST['URL']
        brl.rank = request.POST['Rank']
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Updated Successfully'}))


def get_shopcontacts(request):
    data_arr = []
    md = ManageDealer()
    if request.method == 'GET':
        data = md.getcontacts(request.session.get("dealer_id"))
        for obj in data:
            dic = {}
            dic['id'] = obj.id
            dic['Name'] = obj.name
            dic['Email'] = obj.email
            dic['Phone-WK'] = obj.phone_work
            dic['Phone-Cell'] = obj.phone_cell
            data_arr.append(dic)
    return HttpResponse(json.dumps(data_arr))

@csrf_exempt
def add_shopcontacts(request):
    if request.method == "POST":
        brl = ShopsContact(name = request.POST['Name'] ,
                           email = request.POST['Email'],
                           phone_cell = request.POST['Phone-Cell'],
                           phone_work = request.POST['Phone-WK'],
                           shop_id = request.session.get("dealer_id"))
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Added Successfully'}))

@csrf_exempt
def delete_shopcontacts(request):
    if request.method == "POST":
        ShopsContact.objects.get(id= request.POST['id']).delete()
       
    return HttpResponse(json.dumps({'message' : 'Deleted Successfully'}))
@csrf_exempt
def update_shopcontacts(request):
    if request.method == "POST":
        brl = ShopsContact.objects.get(id= request.POST['id'])
        brl.name = request.POST['Name']
        brl.email = request.POST['Email']
        brl.phone_work = request.POST['Phone-WK']
        brl.phone_cell = request.POST['Phone-Cell']
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Updated Successfully'}))

def get_marketing(request):
    data_arr = []
    md = ManageDealer()
    if request.method == 'GET':
        data = md.getotheremails(request.session.get("dealer_id"), "marketing")
        for obj in data:
            dic = {}
            dic['id'] = obj.id
            dic['Email'] = obj.email
            data_arr.append(dic)
    return HttpResponse(json.dumps(data_arr))

def get_feedback(request):
    data_arr = []
    md = ManageDealer()
    if request.method == 'GET':
        data = md.getotheremails(request.session.get("dealer_id"), "feedback")
        for obj in data:
            dic = {}
            dic['id'] = obj.id
            dic['Email'] = obj.email
            data_arr.append(dic)
    return HttpResponse(json.dumps(data_arr))

def get_serviceemail(request):
    data_arr = []
    md = ManageDealer()
    if request.method == 'GET':
        data = md.getotheremails(request.session.get("dealer_id"), "service")
        for obj in data:
            dic = {}
            dic['id'] = obj.id
            dic['Email'] = obj.email
            data_arr.append(dic)
    return HttpResponse(json.dumps(data_arr))

def get_sms(request):
    data_arr = []
    md = ManageDealer()
    if request.method == 'GET':
        data = md.getsmsno(request.session.get("dealer_id"))
        for obj in data:
            dic = {}
            dic['id'] = obj.id
            dic['SMS-Number'] = obj.sms_no
            data_arr.append(dic)
    return HttpResponse(json.dumps(data_arr))

@csrf_exempt
def add_marketing(request):
    if request.method == "POST":
        brl = ShopOtherEmails(email = request.POST['Email'] , type = "marketing" ,shop_id = request.session.get("dealer_id"))
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Added Successfully'}))

@csrf_exempt
def add_feedback(request):
    if request.method == "POST":
        brl = ShopOtherEmails(email = request.POST['Email'] , type = "feedback" ,shop_id = request.session.get("dealer_id"))
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Added Successfully'}))

@csrf_exempt
def add_serviceemail(request):
    if request.method == "POST":
        brl = ShopOtherEmails(email = request.POST['Email'] , type = "service" ,shop_id = request.session.get("dealer_id"))
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Added Successfully'}))

@csrf_exempt
def delete_email(request):
    if request.method == "POST":
        ShopOtherEmails.objects.get(id= request.POST['id']).delete()
       
    return HttpResponse(json.dumps({'message' : 'Deleted Successfully'}))
@csrf_exempt
def update_email(request):
    if request.method == "POST":
        brl = ShopOtherEmails.objects.get(id= request.POST['id'])
        brl.email = request.POST['Email']
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Updated Successfully'}))

@csrf_exempt
def add_sms(request):
    if request.method == "POST":
        brl = ShopSMS(sms_no = request.POST['SMS-Number'] ,shop_id = request.session.get("dealer_id"))
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Added Successfully'}))

@csrf_exempt
def delete_sms(request):
    if request.method == "POST":
        ShopSMS.objects.get(id= request.POST['id']).delete()
       
    return HttpResponse(json.dumps({'message' : 'Deleted Successfully'}))
@csrf_exempt
def update_sms(request):
    if request.method == "POST":
        brl = ShopSMS.objects.get(id= request.POST['id'])
        brl.sms_no = request.POST['SMS-Number']
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Updated Successfully'}))


def get_shophrs(request):
    data_arr = []
    md = ManageDealer()
    if request.method == 'GET':
        data = md.getshophrs(request.session.get("dealer_id"))
        for obj in data:
            dic = {}
            dic['id'] = obj.id
            dic['Day'] = obj.day
            dic['From'] = obj.time_from.strftime('%I:%M %p')
            dic['To'] = obj.time_to.strftime('%I:%M %p')
            data_arr.append(dic)
    return HttpResponse(json.dumps(data_arr))


@csrf_exempt
def add_shophrs(request):
    if request.method == "POST":
        try:
            brl = ShopHours.objects.get(day = request.POST['Day'],shop_id = request.session.get("dealer_id"))
            return HttpResponse(json.dumps({'message' : 'Shop Hour Already Exist Please Edit The Existing One'}))
        except ShopHours.DoesNotExist:    
            brl = ShopHours(day = request.POST['Day'],
                            time_from = datetime.datetime.strptime(request.POST['From'], '%I:%M %p').time().strftime("%H:%M"),
                            time_to = datetime.datetime.strptime(request.POST['To'], '%I:%M %p').time().strftime("%H:%M") ,
                            shop_id = request.session.get("dealer_id"))
            brl.save()
            return HttpResponse(json.dumps({'message' : 'Shop Hour Saved'}))

@csrf_exempt
def delete_shophrs(request):
    if request.method == "POST":
        ShopHours.objects.get(id= request.POST['id']).delete()
       
    return HttpResponse(json.dumps({'message' : 'Deleted Successfully'}))
@csrf_exempt
def update_shophrs(request):
    if request.method == "POST":
        brl = ShopHours.objects.get(id= request.POST['id'])
        brl.day = request.POST['Day']
        brl.time_from = datetime.datetime.strptime(request.POST['From'], '%I:%M %p').time().strftime("%H:%M")
        brl.time_to = datetime.datetime.strptime(request.POST['To'], '%I:%M %p').time().strftime("%H:%M")
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Updated Successfully'}))


def get_holidays(request):
    data_arr = []
    md = ManageDealer()
    if request.method == 'GET':
        data = md.getholidays(request.session.get("dealer_id"))
        for obj in data:
            dic = {}
            dic['id'] = obj.id
            dic['Description'] = obj.description
            dic['Date'] = obj.date.strftime("%m/%d/%Y")
            data_arr.append(dic)
    return HttpResponse(json.dumps(data_arr))


@csrf_exempt
def add_holiday(request):
    if request.method == "POST":
        date = request.POST['Date']
        brl = ShopHolidays(description = request.POST['Description'],
                           date = date,
                           shop_id = request.session.get("dealer_id"))
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Added Successfully'}))

@csrf_exempt
def delete_holiday(request):
    if request.method == "POST":
        ShopHolidays.objects.get(id= request.POST['id']).delete()
       
    return HttpResponse(json.dumps({'message' : 'Deleted Successfully'}))

@csrf_exempt
def update_holiday(request):
    if request.method == "POST":
        date = request.POST['Date']
        brl = ShopHolidays.objects.get(id= request.POST['id'])
        brl.description = request.POST['Description']
        brl.date = date
        brl.save()
    return HttpResponse(json.dumps({'message' : 'Updated Successfully'}))

def get_user_advisor_form(request):
    template = 'manage/adduser.html'
    nudform = NewUserAdvisorForm(request.session.get("dealer_id"))
    if request.method == "GET":
        return render(request,template,{'nud':nudform});
    
@csrf_exempt
def add_user_advisor(request):
    date = datetime.datetime.now()
    md = ManageDealer()
    customer_factory = CustomerServicesFactory()
    userservice = customer_factory.get_instance("user")
    template = 'manage/mainuat.html'
    error = None
    if request.method == "POST":
        try:
            try:
                user= User.objects.get(username=request.POST['username'])
                raise SuspiciousOperation('User already Exists')
            except User.DoesNotExist:
                
                    if request.POST['email']!="":
                        emailexist = userservice.get_user_profile_by_email(request.POST['email'])
                        if emailexist :
                            raise SuspiciousOperation('User with given email number already exists')
                    if request.POST['phone1']!="":
                        phone1exist = userservice.get_user_profile_by_phone(request.POST['phone1'])
                        if phone1exist :
                            raise SuspiciousOperation('User with given phone1 number already exists')
                    if request.POST['phone2']!="":
                        phone2exist = userservice.get_user_profile_by_phone(request.POST['phone2'])
                        if phone2exist :
                            raise SuspiciousOperation('User with given phone2 number already exists')
                        
                    user = User(username=request.POST['username'])
                    user.set_password(request.POST['password'])
                    user.save()
                    g = Group.objects.get(id=request.POST['role']) 
                    g.user_set.add(user)
                    
                    userp = UserProfile(user=user,first_name=request.POST['first'],last_name=request.POST['last'],email_1=request.POST['email'],phone_number_1=request.POST['phone1'],
                                phone_number_2=request.POST['phone2'], employee_no = request.POST['employee'] ,consumer_reserver= request.POST['reserve'], dealer_id = request.session.get("dealer_id"))
                    if request.FILES:
                        userp.avatar = request.FILES['adv_img']
                    userp.save()
                    teams = map(int, request.POST.getlist('team'))
                    for team in teams:
                        ta = TeamAdvisors(team_id_id = team, advisor = user , created_by_id = request.session.get("dealer_id") ,created_at = date )
                        ta.save()
                    capacity = json.loads(request.POST['capacity'])
                    adv_cap=AdvisorCapacity(monday=int(capacity['cM']),tuesday=int(capacity['cT']),wednesday=int(capacity['cW']),thursday=int(capacity['cTh']),friday=int(capacity['cF']),saturday=int(capacity['cS']),advisor = user , shop_id=request.session.get("dealer_id"))
                    adv_cap.save()
                    restrictions = json.loads(request.POST['restrictions'])
                    for rst in restrictions:
                        Adv_rst = AdvisorRestrictions(advisor = user , type = rst['r_type'] , repeat = rst['r_repeat'])
                        Adv_rst.save()
                        if 'r_stime' in rst and rst['r_stime']:
                            Adv_rst.start_time = rst['r_stime']
                            Adv_rst.save()
                        if 'r_etime' in rst and rst['r_etime']:
                            Adv_rst.end_time = rst['r_etime']
                            Adv_rst.save()
                        if 'r_sdate' in rst and rst['r_sdate']:
                            Adv_rst.start_date = rst['r_sdate']
                            Adv_rst.save()
                        if 'r_edate' in rst and rst['r_edate']:
                            Adv_rst.end_date = rst['r_edate']
                            Adv_rst.save()
                        days = map(int, rst['r_days'])
                        md.set_Restrictiondays(Adv_rst , days)
                        success = "User added Successfully"
        except SuspiciousOperation,e:
                error = str(e)
                success = False
    adv_users = UserProfile.objects.filter(user__groups__id = 4 , dealer_id =request.session.get("dealer_id") )
    app_users = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user__groups__id=4)
    teamslist = Team.objects.filter(created_by_id = request.session.get("dealer_id"))
    return render(request , template ,{'advs' : adv_users , 'app_users' : app_users , 'teaml':teamslist,"error":error,"success":success} )

@csrf_exempt    
def get_edit_view_useradvisor(request):
    template = 'manage/editadvisor.html'
    md = ManageDealer()
    if request.method == "POST":
        user = md.get_user_profile_details(request.POST['id'])
        avatar = user['image']
        enud = NewUserAdvisorForm(request.session.get("dealer_id"),initial = user)
        capacity = md.get_capacity(request.POST['id'])
        restrictions = md.get_restrictions(request.POST['id'])
        
    return render(request,template,{'avatar':avatar,'enud' : enud ,'cap':capacity , 'restrictions':restrictions,"edituser":user })

@csrf_exempt
def edit_user_advisor(request):
    date = datetime.datetime.now()
    md = ManageDealer()
    template = 'manage/mainuat.html'
    customer_factory = CustomerServicesFactory()
    userservice = customer_factory.get_instance("user")
    error = None
    try:
        if request.method == "POST":
            user = User.objects.get(id=request.POST['user_id'])
            if request.POST['email']!="":
                        emailexist = userservice.get_user_profile_by_email(request.POST['email'])
                        if emailexist and emailexist.id !=user.userprofile.id :
                                raise SuspiciousOperation('User with given email number already exists')
                        if request.POST['phone1']!="":
                            phone1exist = userservice.get_user_profile_by_phone(request.POST['phone1'])
                            if phone1exist and phone1exist.id !=user.userprofile.id :
                                raise SuspiciousOperation('User with given phone1 number already exists')
                        if request.POST['phone2']!="" :
                            phone2exist = userservice.get_user_profile_by_phone(request.POST['phone2'])
                            if phone2exist and phone2exist.id !=user.userprofile.id:
                                raise SuspiciousOperation('User with given phone2 number already exists')
            
    #         if request.POST['username']:
    #             user.username = request.POST['username']
            if request.POST['password']:
                user.set_password(request.POST['password'])
            user.userprofile.first_name = request.POST['first']
            user.userprofile.last_name = request.POST['last']
            user.userprofile.email_1 = request.POST['email']
            user.userprofile.phone_number_1 = request.POST['phone1']
            user.userprofile.phone_number_2 = request.POST['phone2']
            user.userprofile.employee_no = request.POST['employee']
            user.userprofile.consumer_reserver = request.POST['reserve']
            if request.FILES:
                user.userprofile.avatar = request.FILES['adv_img']
            user.userprofile.save()
            user.save()
            user.groups.clear()
            g = Group.objects.get(id=request.POST['role']) 
            g.user_set.add(user)
            teams = map(int, request.POST.getlist('team'))
            if teams:
                for team in teams:
                    try:
                        TeamAdvisors.objects.get(advisor = user, team_id_id = team)
                    except TeamAdvisors.DoesNotExist:
                        ta = TeamAdvisors(team_id_id = team, advisor = user , created_by_id = request.session.get("dealer_id") ,created_at = date )
                        ta.save()
                TeamAdvisors.objects.filter(advisor = user).exclude(team_id_id__in = teams).delete()
            else:
                TeamAdvisors.objects.filter(advisor = user).delete()
            capacity = json.loads(request.POST['capacity'])
            if capacity['id']:
                cap = AdvisorCapacity.objects.get(id = capacity['id'])
                cap.monday = int(capacity['ecM'])
                cap.tuesday = int(capacity['ecT'])
                cap.wednesday = int(capacity['ecW'])
                cap.thursday = int(capacity['ecTh'])
                cap.friday = int(capacity['ecF'])
                cap.saturday = int(capacity['ecS'])
                cap.save() 
            else:
                if not capacity['ecM']:
                    capacity['ecM']=1
                if not capacity['ecT']:
                    capacity['ecT']=1
                if not capacity['ecW']:
                    capacity['ecW']=1
                if not capacity['ecTh']:
                    capacity['ecTh']=1
                if not capacity['ecF']:
                    capacity['ecF']=1
                if not capacity['ecS']:
                    capacity['ecS']=1
                adv_cap=AdvisorCapacity(monday=int(capacity['ecM']),tuesday=int(capacity['ecT']),wednesday=int(capacity['ecW']),
                                        thursday=int(capacity['ecTh']),friday=int(capacity['ecF']),saturday=int(capacity['ecS']),advisor = user , shop_id= request.session.get("dealer_id"))
                adv_cap.save()
            restrictions = json.loads(request.POST['restrictions'])
            if restrictions:
                rst_ids = []
                for rst in restrictions:
                    if rst['id']:
                        rst_ids.append(rst['id'])
                        adv_rst  = AdvisorRestrictions.objects.get(id = rst['id'])
                        adv_rst.type = rst['er_type']
                        adv_rst.repeat = rst['er_repeat']
                        if 'er_stime' in rst and rst['er_stime']:
                            adv_rst.start_time = rst['er_stime']
                            adv_rst.save()
                        else:
                            adv_rst.start_time = None
                            adv_rst.save()
                        if 'er_etime' in rst and rst['er_etime']:
                            adv_rst.end_time = rst['er_etime']
                            adv_rst.save()
                        else:
                            adv_rst.end_time = None
                            adv_rst.save()
                        if 'er_sdate' in rst and rst['er_sdate']:
                            adv_rst.start_date = rst['er_sdate']
                            adv_rst.save()
                        else:
                            adv_rst.start_date = None
                            adv_rst.save()
                        if 'er_edate' in rst and rst['er_edate']:
                            adv_rst.end_date = rst['er_edate']
                            adv_rst.save()
                        else:
                            adv_rst.end_date = None
                            adv_rst.save()
                        days = map(int, rst['er_days'])
                        md.set_Restrictiondays(adv_rst , days)
                    else:
                        Adv_rst = AdvisorRestrictions(advisor = user , type = rst['er_type'] , repeat = rst['er_repeat'])
                        Adv_rst.save()
                        rst_ids.append(Adv_rst.id)
                        if 'er_stime' in rst and rst['er_stime']:
                            Adv_rst.start_time = rst['er_stime']
                            Adv_rst.save()
                        if 'er_etime' in rst and rst['er_etime']:
                            Adv_rst.end_time = rst['er_etime']
                            Adv_rst.save()
                        if 'er_sdate' in rst and rst['er_sdate']:
                            Adv_rst.start_date = rst['er_sdate']
                            Adv_rst.save()
                        if 'er_edate' in rst and rst['er_edate']:
                            Adv_rst.end_date = rst['er_edate']
                            Adv_rst.save()
                        days = map(int, rst['er_days'])
                        md.set_Restrictiondays(Adv_rst , days)
                AdvisorRestrictions.objects.filter(advisor = user).exclude(id__in = rst_ids).delete()
            else:
                AdvisorRestrictions.objects.filter(advisor = user).delete()
            success = "User edited Successfully"
    except SuspiciousOperation,e:
                error = str(e)
                success = False   
    adv_users = UserProfile.objects.filter(user__groups__id = 4 , dealer_id =request.session.get("dealer_id") )
    app_users = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user__groups__id=4)
    teamslist = Team.objects.filter(created_by_id = request.session.get("dealer_id"))
    return render(request , template ,{'advs' : adv_users , 'app_users' : app_users , 'teaml':teamslist,"error":error,"success":success} )

@csrf_exempt
def add_team(request):
    template = 'manage/mainuat.html'
    date = datetime.datetime.now()
    if request.method == "POST":
        team = Team(name = request.POST["name"] , created_by_id = request.session.get("dealer_id") , created_at = date)
        team.save()
    adv_users = UserProfile.objects.filter(user__groups__id = 4 , dealer_id =request.session.get("dealer_id") )
    app_users = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user__groups__id=4)
    teamslist = Team.objects.filter(created_by_id = request.session.get("dealer_id"))
    return render(request , template ,{'advs' : adv_users , 'app_users' : app_users , 'teaml':teamslist} )    

@csrf_exempt
def edit_team(request):
    template = 'manage/editteam.html'
    if request.method == "POST":
        team_users = TeamAdvisors.objects.filter(team_id_id= request.POST['id'])
        team = Team.objects.get(id=request.POST['id'])
        user_id_list = []
        for tu in team_users:
            user_id_list.append(tu.advisor.id)
        not_in_team = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user_id__in = user_id_list)
    return render(request , template , {'team_users' : team_users , 'not_members' : not_in_team , 'team':team} )


@csrf_exempt
def add_members_team(request):
    template = 'manage/editteam.html'
    if request.method == "POST":
        print request.POST
        team = Team.objects.get(id=request.POST['id'])
        team_members = request.POST.getlist('team_members[]')
        team_members = map(int,team_members)
        for member in team_members:
            ta = TeamAdvisors(team_id_id = request.POST['id'] , advisor_id = member , created_by_id =request.session.get("dealer_id") , created_at = datetime.datetime.now())
            ta.save()
        team_users = TeamAdvisors.objects.filter(team_id_id= request.POST['id'])
        user_id_list = []
        for tu in team_users:
            user_id_list.append(tu.advisor.id)
        not_in_team = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user_id__in = user_id_list)
    return render(request , template , {'team_users' : team_users , 'not_members' : not_in_team , 'team':team} )


@csrf_exempt
def delete_members_team(request):
    template = 'manage/editteam.html'
    if request.method == "POST":
        team = Team.objects.get(id=request.POST['id'])
        TeamAdvisors.objects.get(id = request.POST['team_mem_id']).delete()
        team_users = TeamAdvisors.objects.filter(team_id_id= request.POST['id'])
        user_id_list = []
        for tu in team_users:
            user_id_list.append(tu.advisor.id)
        not_in_team = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user_id__in = user_id_list)
    return render(request , template , {'team_users' : team_users , 'not_members' : not_in_team , 'team':team} )


@csrf_exempt
def remove_team(request):
    template = 'manage/mainuat.html'
    if request.method == "POST":
        Team.objects.get(id = request.POST['id']).delete()
    adv_users = UserProfile.objects.filter(user__groups__id = 4 , dealer_id =request.session.get("dealer_id") )
    app_users = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user__groups__id=4)
    teamslist = Team.objects.filter(created_by_id = request.session.get("dealer_id"))
    return render(request , template ,{'advs' : adv_users , 'app_users' : app_users , 'teaml':teamslist} ) 

@csrf_exempt
def remove_user_advisor(request):
    template = 'manage/mainuat.html'
    if request.method == "POST":
        user_id = request.POST['id']
        if user_id !=request.user.id:
            user = User.objects.get(id = request.POST['id'])#
            userprofile = UserProfile.objects.get(user_id=request.POST['id'])
            userprofile.delete()
            user.delete()
        else:
            raise SuspiciousOperation('Cannot delete current User')
    adv_users = UserProfile.objects.filter(user__groups__id = 4 , dealer_id =request.session.get("dealer_id") )
    app_users = UserProfile.objects.filter(dealer_id = request.session.get("dealer_id")).exclude(user__groups__id=4)
    teamslist = Team.objects.filter(created_by_id = request.session.get("dealer_id"))
    return render(request , template ,{'advs' : adv_users , 'app_users' : app_users , 'teaml':teamslist} )  


def get_ajax_all_favorites(request): 
    favorites = []
    if request.method == 'GET': 
        dealer_factory = DealerShipServicesFactory()
        dealer_service = dealer_factory.get_instance("dealership")
        favorites = dealer_service.get_all_favorites()   
       
    return JsonResponse({'favorites':favorites}) 

def save_ajax_dealer_favorites(request):
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")
    favorites = []
    template = 'dealership/app/partials/favorites-list.html'
    try:
        if request.method == 'POST':    
            dealer_service.save_dealer_favorites(request.session["dealer_id"], request.POST.get('favorites_id'))          
            favorites = dealer_service.get_dealer_favorites(request.session["dealer_id"])  
    except:
        pass          
    return render(request, template, {'favorites':favorites})

def get_ajax_dealer_favorites(request):
    favorites = []
    try:
        if request.method == 'GET': 
            dealer_factory = DealerShipServicesFactory()
            dealer_service = dealer_factory.get_instance("dealership")
            favorites = dealer_service.get_dealer_favorites(request.session["dealer_id"])  
    except:
        pass          
    return JsonResponse({'favorites':favorites}) 

@csrf_exempt
def add_package(request):
    template = 'manage/inspections.html'
    if request.method == "POST":
        pack = InspectionPackage(package = request.POST['pack_name'] , dealer_id = request.session["dealer_id"])
        pack.save()
    package = InspectionPackage.objects.filter(dealer_id = request.session["dealer_id"])
    pform = PackageForm()
    catform = CategoryForm()
    iform = ItemForm()
    items_all = InspectionItems.objects.all()
    return render(request , template ,{'packages':package,'pform':pform, 'catform':catform , 'iform':iform ,'items_all':items_all})

@csrf_exempt
def add_category(request):
    if request.method == "POST":
        print request.POST
        cat = InspectionCatagories(category = request.POST['cat_name'] , package_id = request.POST['pack'])
        cat.save()
        for obj in request.POST.getlist('itemlist'):
            catitems = InspectionCategoriesItems(category_id = cat.id , item_id = obj)
            catitems.save()
    
    return JsonResponse({'pack_id': cat.package_id , 'cat_id' : cat.id})

@csrf_exempt
def get_category(request):
    template = "manage/categorylist.html"
    if request.method == "POST":
        category = InspectionCatagories.objects.filter(package_id = request.POST['id'])
    return render(request, template, {'category': category})

@csrf_exempt
def get_inspection_items(request):
    template = "manage/inspection_details.html"
    if request.method == "POST":
        cat_items = InspectionCategoriesItems.objects.filter(category_id = request.POST['id'])
        items_id = []
        for obj in cat_items:
            items_id.append(obj.item.id)
        items = InspectionItems.objects.exclude(id__in = items_id )
    return render(request, template, {'cat_items':cat_items , 'items':items})

@csrf_exempt
def add_category_inspection_item(request):
    template = "manage/inspection_details.html"
    print request.POST
    if request.method == "POST":
        for obj in request.POST.getlist('items[]'):
            catitems = InspectionCategoriesItems(category_id = request.POST['cat_id'] , item_id = obj)
            catitems.save()
        cat_items = InspectionCategoriesItems.objects.filter(category_id = request.POST['cat_id'])
        items_id = []
        for obj in cat_items:
            items_id.append(obj.item.id)
        items = InspectionItems.objects.exclude(id__in = items_id )
    return render(request, template, {'cat_items':cat_items , 'items':items})

@csrf_exempt
def remove_category_inspection_item(request):
    template = "manage/inspection_details.html"
    if request.method == "POST":
        for obj in request.POST.getlist('items[]'):
            InspectionCategoriesItems.objects.get(id=obj).delete()
        cat_items = InspectionCategoriesItems.objects.filter(category_id = request.POST['cat_id'])
        items_id = []
        for obj in cat_items:
            items_id.append(obj.item.id)
        items = InspectionItems.objects.exclude(id__in = items_id )
    return render(request, template, {'cat_items':cat_items , 'items':items})


@csrf_exempt
def add_new_item(request):
    template = "manage/inspection_details.html"
    if request.method == "POST":
        item = InspectionItems(item = request.POST['item_name'])
        item.save()
        catitems = InspectionCategoriesItems(category_id = request.POST['cat_id'] , item_id = item.id)
        catitems.save()
        cat_items = InspectionCategoriesItems.objects.filter(category_id = request.POST['cat_id'])
        items_id = []
        for obj in cat_items:
            items_id.append(obj.item.id)
        items = InspectionItems.objects.exclude(id__in = items_id )
    return render(request, template, {'cat_items':cat_items , 'items':items})

@csrf_exempt
def edit_flags(request):
    template = "manage/flags.html"
    md = ManageDealer()
    nfform = NewFlagForm()
    if request.method == "POST":
        try:
            flag = Flags.objects.get(id=request.POST['eflagid'])
        except Flags.DoesNotExist:
            flag= None
        if flag:
            flag.name = request.POST['eflagname']
            flag.color = request.POST['eflagcolor']
            flag.type = request.POST['eflagtype']
            if request.POST['approvalRequired'] == "yes" and request.POST['ecfacing'] == "1" and request.POST['eflagtype'] == "3":
                dealer = Dealer.objects.get(id=request.session["dealer_id"])
                dealer.approval_needed_flag_id = flag.id
                dealer.save()
            if request.POST['ecfacing'] == "1":
                flag.customer_facing = True
            else:
                flag.customer_facing = False
            flag.save()
    flag_types = Flags.objects.filter(dealer_id=request.session["dealer_id"]).values('type').order_by('type').distinct()
    flag_data = []
    for obj in flag_types:
        fdic={}
        fdic["type"] = obj["type"]
        fdic["data"] = md.get_flag_data(obj["type"],request.session["dealer_id"])
        flag_data.append(fdic)
    
    return render(request, template, {'flags':flag_data , 'nfform':nfform})

@csrf_exempt
def add_flags(request):
    template = "manage/flags.html"
    md = ManageDealer()
    nfform = NewFlagForm()
    if request.method == "POST":
        flag = Flags(dealer_id=request.session["dealer_id"],name = request.POST['flag_name'] ,type = request.POST['aflagtype'], color = request.POST['aflagcolor'])
        flag.customer_facing = True if request.POST['acfacing']  == 1 and request.POST['aflagtype']  == "3" else False
#             True
#         else:
#             flag.customer_facing = False
        flag.save()
        if request.POST['approvalRequired'] == "yes" and request.POST['acfacing']  == "1" and request.POST["aflagtype"] == "3":
                dealer = Dealer.objects.get(id=request.session["dealer_id"])
                dealer.approval_needed_flag_id = flag.id
                dealer.save()
    flag_types = Flags.objects.filter(dealer_id=request.session["dealer_id"]).values('type').order_by('type').distinct()
    flag_data = []
    for obj in flag_types:
        fdic={}
        fdic["type"] = obj["type"]
        fdic["data"] = md.get_flag_data(obj["type"],request.session["dealer_id"])
        flag_data.append(fdic)
    
    return render(request, template, {'flags':flag_data , 'nfform':nfform})

@csrf_exempt
def del_flags(request):
    template = "manage/flags.html"
    md = ManageDealer()
    nfform = NewFlagForm()
    if request.method == "POST":
        Flags.objects.get(id=request.POST['id']).delete()
    flag_types = Flags.objects.filter(dealer_id=request.session["dealer_id"]).values('type').order_by('type').distinct()
    flag_data = []
    for obj in flag_types:
        fdic={}
        fdic["type"] = obj["type"]
        fdic["data"] = md.get_flag_data(obj["type"],request.session["dealer_id"])
        flag_data.append(fdic)
    
    return render(request, template, {'flags':flag_data , 'nfform':nfform})

@csrf_exempt
def get_package_detail(request):
    template = "manage/editpack.html"
    if request.method == "POST":    
        try:  
            pack = InspectionPackage.objects.get(id= request.POST['id'])
        except Exception:
            pack = None
            
        
    return render(request, template, {'pack':pack })

@csrf_exempt
def edit_package(request):
    template = 'manage/inspections.html'
    if request.method == "POST":
        pack = InspectionPackage.objects.get(id = request.POST['pack_id'])
        pack.package = request.POST['pack_name']
        pack.save()
    package = InspectionPackage.objects.filter(dealer_id = request.session["dealer_id"])
    pform = PackageForm()
    catform = CategoryForm()
    iform = ItemForm()
    items_all = InspectionItems.objects.all()
    return render(request , template ,{'packages':package,'pform':pform, 'catform':catform , 'iform':iform ,'items_all':items_all})

@csrf_exempt
def delete_package(request):
    return
    template = 'manage/inspections.html'
    if request.method == "POST":
        pack = InspectionPackage.objects.get(id = request.POST['pack_id']).delete()
    package = InspectionPackage.objects.filter(dealer_id = request.session["dealer_id"])
    pform = PackageForm()
    catform = CategoryForm()
    iform = ItemForm()
    items_all = InspectionItems.objects.all()
    return render(request , template ,{'packages':package,'pform':pform, 'catform':catform , 'iform':iform ,'items_all':items_all})


@csrf_exempt
def get_cat_edit(request):
    template = "manage/editcatlist.html"
    if request.method == "POST":      
        cat = InspectionCatagories.objects.filter(package_id = request.POST['id'])
    return render(request, template, {'cat':cat })


@csrf_exempt
def edit_cat(request):
    template = 'manage/inspections.html'
    if request.method == "POST":
        cat = InspectionCatagories.objects.get(id = request.POST['cat_id'])
        cat.category = request.POST['cat_name']
        cat.save()
    package = InspectionPackage.objects.filter(dealer_id = request.session["dealer_id"])
    pform = PackageForm()
    catform = CategoryForm()
    iform = ItemForm()
    items_all = InspectionItems.objects.all()
    return render(request , template ,{'packages':package,'pform':pform, 'catform':catform , 'iform':iform ,'items_all':items_all})

@csrf_exempt
def delete_cat(request):
    template = 'manage/inspections.html'
    if request.method == "POST":
        cat = InspectionCatagories.objects.get(id = request.POST['cat_id']).delete()
    package = InspectionPackage.objects.filter(dealer_id = request.session["dealer_id"])
    pform = PackageForm()
    catform = CategoryForm()
    iform = ItemForm()
    items_all = InspectionItems.objects.all()
    return render(request , template ,{'packages':package,'pform':pform, 'catform':catform , 'iform':iform ,'items_all':items_all})


@csrf_exempt
def delete_category_inspection_item(request):
    template = "manage/inspection_details.html"
    print request.POST
    if request.method == "POST":
        for obj in request.POST.getlist('items[]'):
            catitems = InspectionItems.objects.get(id = obj).delete()
        cat_items = InspectionCategoriesItems.objects.filter(category_id = request.POST['cat_id'])
        items_id = []
        for obj in cat_items:
            items_id.append(obj.item.id)
        items = InspectionItems.objects.exclude(id__in = items_id )
    return render(request, template, {'cat_items':cat_items , 'items':items})