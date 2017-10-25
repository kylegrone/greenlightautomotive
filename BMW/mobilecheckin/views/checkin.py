from base64 import b64decode
import base64
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

import cStringIO as StringIO
from dealership.decorators import *
from dealership.factories import DealerShipServicesFactory
from dealership.models import *
from dealership.services.appointmentservices import AppointmentService as AS
from dealership.services.emailservice import EmailService
from dealership.services.vehicleservices import VehicleService
from mobilecheckin import confg
from mobilecheckin.decorators import checkin_access_check


# Create your views here.
@checkin_access_check
def index(request,appointment_id):
    template= "mobilecheckin/checkin/checkin.html"
    date_time = timezone.now()
    dservice = AS()
    try:
        app_details = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        raise Http404
    status = AppointmentStatus.objects.get(name="In Progress")
    if app_details.appointment_status == status:
        if app_details.checkin_time:
            time_left = dservice.get_in_progress_remaining_time(app_details.checkin_time)
    else:  
        time_left = {'min' : 5 , 'sec': 0}      
        app_details.appointment_status = status
        app_details.checkin_time = date_time
        app_details.save()
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    
    return render(request, template, {'app_details' : app_details,'app_services' : app_service, 'time_left':time_left,'dealer_code':request.session["dealer_code"]})

@checkin_access_check
def get_odo(request,appointment_id):
    dservice = AS()
    try:
        app_details = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        raise Http404
    template= "mobilecheckin/checkin/odovin.html"
   
    return render(request, template, {"app_details":app_details}) 
 
@checkin_access_check   
def get_serviceandrepair(request, appointment_id):
    template= "mobilecheckin/checkin/servicerepair.html"
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    appt = Appointment.objects.get(id=appointment_id)
    total_cost = 0
    for obj in app_service:
        total_cost += obj.price
    serrep = ServiceRepair.objects.filter(dealer_id = appt.dealer_id).all()
    return render(request, template, {'app_services' : app_service ,
                                      'totalcost':total_cost , 
                                      'serrep':serrep})
@checkin_access_check
def get_reviewandsign(request,appointment_id):
    template= "mobilecheckin/checkin/reviewandsign.html"
    app_details = Appointment.objects.get(id=appointment_id)
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    total_cost = 0
    for obj in app_service:
        total_cost += obj.price
    wlkarnd_details = walkaroundnotes.objects.filter(appointment_id=appointment_id)
    return render(request, template, {'app_details' : app_details,'app_services' : app_service , 'totalcost' : total_cost,
                                      'wlkarnd_details' : wlkarnd_details})

@csrf_exempt
def get_odometer_history(request,appointment_id):
    template= "mobilecheckin/checkin/odohistory.html"
    vehicle_sevice = VehicleService()
    if request.method == "POST":
        if request.POST['odo']:
            appt_detail = Appointment.objects.get(id = appointment_id)
            cv = None
            try:
                cv = CustomerVehicle.objects.get(id = appt_detail.vehicle.id)
                cv.milage = int(request.POST['odo'])
                cv.save()
            except Exception,e:
                print e
            appt_detail.odometer_reading = request.POST['odo']
            if request.POST.get('odo_data') and request.POST.get('odo_data',"").strip()!="":
#                 appt_detail.odometer_data = request.POST['odo_data']
                filename = str(appointment_id)+"_apt_img.png"
                vehicle_sevice.get_img_from_data(request.POST['odo_data'],filename)
                appt_detail.odometer_image = "./"+filename
            appt_detail.save()
        odo_history = Appointment.objects.filter(vehicle_id = appt_detail.vehicle.id, start_time__lt = appt_detail.start_time)
        return render(request, template, {'odo_history' : odo_history })
    
@csrf_exempt
def save_vin(request,appointment_id):
    service = VehicleService()
    if request.method == "POST":
        if request.POST['vin']:
            
            appt_detail = Appointment.objects.get(id = appointment_id)
            cv = None
            try:
                cv = CustomerVehicle.objects.get(id = appt_detail.vehicle.id)
                cv.vin_number = request.POST['vin']
                cv.save()
            except Exception,e:
                print e
        if request.POST['vin_data']:
            appt_detail = Appointment.objects.get(id = appointment_id)
            cv = None
            try:
                cv = CustomerVehicle.objects.get(id = appt_detail.vehicle.id)
                service.save_vehicle_vin_data(cv, request.POST['vin_data'])
#                 cv.vin_data = request.POST['vin_data']
#                 cv.save()
            except Exception,e:
                print e   
        return HttpResponse(json.dumps({'message' : 'Vin Added Successfully'}))

@csrf_exempt    
def get_service_repair_list(request):
    template = "mobilecheckin/checkin/servicerepairlist.html"
    if request.method == "POST":
        if request.POST['type'] == "all":
            serrep = ServiceRepair.objects.all()
        else:
            serrep = ServiceRepair.objects.filter(type= request.POST['type'])
        return render(request, template, {'serrep':serrep })
    
@csrf_exempt
def add_service_repair(request,appointment_id):
    template = "mobilecheckin/checkin/appt_service_list.html"
    if request.method == "POST":
        service = ServiceRepair.objects.get(id=request.POST['id'])
        app =AppointmentService(appointment_id = appointment_id , service_id = request.POST['id'])
        app.price = request.POST.get("price",service.price)
        app.desc = request.POST.get("desc","")
        app.save()
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    total_cost = 0
    for obj in app_service:
        total_cost += obj.price
    return render(request, template, {'app_services' : app_service ,'totalcost':total_cost })
    
@csrf_exempt
def remove_service_repair(request,appointment_id):
    template = "mobilecheckin/checkin/appt_service_list.html"
    if request.method == "POST":
        AppointmentService.objects.get(id=request.POST['id']).delete()
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    total_cost = 0
    for obj in app_service:
        total_cost += obj.price
    return render(request, template, {'app_services' : app_service ,'totalcost':total_cost })

@csrf_exempt
def update_service_repair(request,appointment_id):
    template = "mobilecheckin/checkin/appt_service_list.html"
    if request.method == "POST":
        appt_update =  AppointmentService.objects.get(id=request.POST['id'])
        service = appt_update.service
        appt_update.price = request.POST.get("price",service.price)
        appt_update.desc = request.POST.get("desc","")
        appt_update.save()
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    total_cost = 0
    for obj in app_service:
        total_cost += obj.price
    return render(request, template, {'app_services' : app_service ,'totalcost':total_cost })

@csrf_exempt    
def get_by_name_service_repair(request):
    template = "mobilecheckin/checkin/servicerepairlist.html"
    if request.method == "POST":
        serrep = ServiceRepair.objects.filter(name__contains= request.POST['key'])
        return render(request, template, {'serrep':serrep })

@checkin_access_check
def get_walkaround(request,appointment_id):
    template = "mobilecheckin/checkin/walkaround.html"
    appointment = Appointment.objects.get(id = appointment_id)
    vehicles = CustomerVehicle.objects.filter(user_id= appointment.customer.id)
    map_image = [] 
    vehicle_parts = []
    services = ServiceRepair.objects.all()
    media = walkaroundnotes.objects.filter(appointment_id = appointment_id)
    if appointment.vehicle:
        vehicle_parts = VehicleParts.objects.filter(vehicle_id = appointment.vehicle.vehicle.id)
        if not vehicle_parts:
            vehicle_parts = VehicleParts.objects.filter(vehicle= None)
        wlk_veh_image = WalkaroundVehicleImage.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , dealer_id = request.session["dealer_id"])
        if not wlk_veh_image:
            wlk_veh_image = WalkaroundVehicleImage.objects.filter(vehicle = None,dealer_id = request.session["dealer_id"])
        for obj in wlk_veh_image:
            veh_img_map = {}
            veh_img_map['veh_img'] = obj
            veh_img_map['map'] = WalkaroundVehicleMap.objects.filter(vehicleimage = obj)
            map_image.append(veh_img_map)
        thumbnails =  wlk_veh_image
    else:
        vehicle_parts = VehicleParts.objects.filter(vehicle= None)
        wlk_veh_image = WalkaroundVehicleImage.objects.filter(vehicle = None,dealer_id = request.session["dealer_id"])
        for obj in wlk_veh_image:
            veh_img_map = {}
            veh_img_map['veh_img'] = obj
            veh_img_map['map'] = WalkaroundVehicleMap.objects.filter(vehicleimage = obj)
            map_image.append(veh_img_map)
        thumbnails =  wlk_veh_image
    return render(request, template, {'vehicles' : vehicles , 'appointment':appointment , 'services':services,
                                       'map_image' : map_image, 'thumbnails':thumbnails ,'v_parts' : vehicle_parts,
                                       "media":media
                                       })

@csrf_exempt
def add_notes_walkaround(request,appointment_id):
    if request.method == "POST":
        
        if request.POST['other_category'] == "":
            request.POST['other_category'] = "Damage"
        wlknotes = walkaroundnotes(appointment_id = appointment_id , notes = request.POST['note'],
                        type = request.POST['type'] , image_name = request.POST['image_name'] ,
                        other_category = request.POST['other_category'] , other_type = request.POST['other_type'])
        wlknotes.save()
        if 'image' in request.POST:
            try:
                img  = request.POST['image'].split('base64,')
                image_data = b64decode(img[1])
                wlknotes.image = ContentFile(image_data, 'image.png')
                wlknotes.save()
            except Exception,e:
                print e   
        return HttpResponse(json.dumps({'message' : 'Notes Added Successfully'}))

def get_walkaround_media(request,appointment_id):
    template = "mobilecheckin/checkin/walkaroundmedia.html"
    if request.method=="GET":
        media = walkaroundnotes.objects.filter(appointment_id = appointment_id)
        
        return render(request, template , {'media' : media})
    
def get_walkaround_notes(request,appointment_id):
    template = "mobilecheckin/checkin/walkaroundnotes.html"
    if request.method=="GET":
        notes = walkaroundnotes.objects.filter(appointment_id = appointment_id)
        
        return render(request, template , {'notes' : notes})

@csrf_exempt
def get_selected_vehicle(request):
    template = "mobilecheckin/checkin/walkaroundvehicleselect.html" 
    if request.method=="POST":
        services = ServiceRepair.objects.all()
        vehicle_parts = VehicleParts.objects.filter(vehicle_id = request.POST['id'])
        if not vehicle_parts:
            vehicle_parts = VehicleParts.objects.filter(vehicle = None)
        
        return render(request, template, {'services':services,'v_parts' : vehicle_parts})

@csrf_exempt
def get_selected_vehicle_map(request):
    template = "mobilecheckin/checkin/imagemap.html"
    if request.method =="POST":
        map_image = []
        wlk_veh_image = WalkaroundVehicleImage.objects.filter(vehicle_id = request.POST['id'],dealer_id = request.session["dealer_id"])
        if not wlk_veh_image:
            wlk_veh_image = WalkaroundVehicleImage.objects.filter(vehicle = None,dealer_id = request.session["dealer_id"])
        for obj in wlk_veh_image:
            veh_img_map = {}
            veh_img_map['veh_img'] = obj
            veh_img_map['map'] = WalkaroundVehicleMap.objects.filter(vehicleimage = obj)
            map_image.append(veh_img_map)
        thumbnails =  wlk_veh_image
        return render(request, template, {'map_image' : map_image , 'thumbnails':thumbnails})

@csrf_exempt
def add_walkaround_initials(request,appointment_id):
    if request.method == "POST":
        wlk_initials = WalkaroundInitials(appointment_id = appointment_id , type = request.POST['type'] , 
                                          initials = request.POST['initials'] )
        wlk_initials.save()
        return HttpResponse(json.dumps({'message' : 'Initials Added'}))
    
@csrf_exempt
def accept_appointment_summary(request,appointment_id):
        dealer_factory = DealerShipServicesFactory()
        notificationservice = dealer_factory.get_instance("notification")
        if request.method == "POST":
            ro = RO()
            appnt =Appointment.objects.get(id = appointment_id)
            appnt_status = AppointmentStatus.objects.get(name = "Checked in")
            appnt.appointment_status = appnt_status
            appnt.customer_signatures = request.POST['sign']
            appnt.save()
            if not appnt.ro:
                ro.ro_number = appnt.id
                ro.rfid_tag = appnt.id
                ro.ro_date = timezone.now()
                ro.save()
                appnt.ro = ro
                appnt.save()
            name = appnt.customer.first_name+" "+appnt.customer.last_name
            main_site_url = settings.SITE_MAIN_URL+reverse('customer:main')+"?dealer_code=" +appnt.dealer.dealer_code
            context = {"appointment_id" : appointment_id , 
                       "domain" : settings.SITE_MAIN_URL+reverse('customer:status_alert_index',
                                                                 kwargs={'appointment_id': appointment_id}), 
                       "name":name,
                       "dealer_name":appnt.dealer.name,
                       "address":appnt.dealer.address_line1+" "+appnt.dealer.address_line2,
                       "main_site_url":main_site_url
                       }
            params = json.dumps(context)  
            
            try:
                notificationservice.send_dealer_based_notification(appnt.dealer,appnt.customer,params,"status_url",send_email=True,send_text=False)
            except Exception,e:
                print e
            
            if request.POST['send_email'] == 'true':
                params = get_walkindata(appointment_id)
                attachment = None
                pdf_file = pdf_processing('mobilecheckin/checkin/pdf.html', appointment_id, request.session["dealer_code"])
                if pdf_file:
                    attachment = pdf_file.getvalue()
                try:
                    notificationservice.send_dealer_based_notification(appnt.dealer,appnt.customer,params,"mobilecheckin_review",send_email=True,send_text=False,attachment=attachment)
                except Exception,e:
                    print e
                return HttpResponse(json.dumps({'message' : 'accepted'}))
        return HttpResponse(json.dumps({'message' : 'accepted'}))
    
@csrf_exempt
def cancle_appointment_summary(request,appointment_id):
    if request.method == "POST":
        appnt =Appointment.objects.get(id = appointment_id)
        appnt_status = AppointmentStatus.objects.get(name = "Cancelled")
        appnt.appointment_status = appnt_status
        appnt.save()
        return HttpResponse(json.dumps({'message' : 'canceled'}))
    
@csrf_exempt
def get_tire_thread(request,appointment_id):
    template= "mobilecheckin/checkin/tirethread.html"
    appointment = Appointment.objects.get(id = appointment_id)
    tirenotes = walkaroundnotes.objects.filter(type="Tires",appointment__vehicle = appointment.vehicle)
    tire_rr = []
    tire_rf = []
    tire_lr = []
    tire_lf = []
    tirenotes = []
    if appointment.vehicle:
        vehicle_parts = VehicleParts.objects.filter(vehicle_id = appointment.vehicle.vehicle.id)
        tirenotes = walkaroundnotes.objects.filter(type="Tires",appointment__vehicle = appointment.vehicle)
        if not vehicle_parts:
            vehicle_parts = VehicleParts.objects.filter(vehicle = None)
        tire_rr = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='RR')
        if not tire_rr:
            tire_rr = VehicleTireWidth.objects.filter(vehicle = None , type='RR')
        tire_rf = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='RF')
        if not tire_rf:
            tire_rf = VehicleTireWidth.objects.filter(vehicle_id = None , type='RF')
        tire_lr = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='LR')
        if not tire_lr:
            tire_lr = VehicleTireWidth.objects.filter(vehicle_id = None , type='LR')
        tire_lf = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='LF')
        if not tire_lf:
            tire_lf = VehicleTireWidth.objects.filter(vehicle_id = None , type='LF')
    else:
        vehicle_parts = VehicleParts.objects.filter(vehicle = None)
        tire_rr = VehicleTireWidth.objects.filter(vehicle = None , type='RR')
        tire_rf = VehicleTireWidth.objects.filter(vehicle_id = None , type='RF')
        tire_lr = VehicleTireWidth.objects.filter(vehicle_id = None , type='LR')
        tire_lf = VehicleTireWidth.objects.filter(vehicle_id = None , type='LF')
        
    
    return render(request, template, {'rr':tire_rr,'rf':tire_rf , 'lr':tire_lr , 'lf':tire_lf , 'tirenote': tirenotes})

@csrf_exempt
def add_tire_notes(request , appointment_id):
    template= "mobilecheckin/checkin/tirethread.html"
    appointment = Appointment.objects.get(id = appointment_id)
    tirenotes = walkaroundnotes.objects.filter(appointment__vehicle = appointment.vehicle)
    print tirenotes
    if request.POST:
        wlknotes = walkaroundnotes(appointment_id = appointment_id , notes = request.POST['notes'],
                        type = "Tires" , RR_id=request.POST['RR'], RF_id=request.POST['RF'], 
                        LR_id=request.POST['LR'], LF_id=request.POST['LF'])
        wlknotes.save()
    tire_rr = []
    tire_rf = []
    tire_lr = []
    tire_lf = []
    tirenotes = []
    if appointment.vehicle:
        tirenotes = walkaroundnotes.objects.filter(type="Tires",appointment__vehicle = appointment.vehicle)
        vehicle_parts = VehicleParts.objects.filter(vehicle_id = appointment.vehicle.vehicle.id)
        if not vehicle_parts:
            vehicle_parts = VehicleParts.objects.filter(vehicle = None)
        tire_rr = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='RR')
        if not tire_rr:
            tire_rr = VehicleTireWidth.objects.filter(vehicle = None , type='RR')
        tire_rf = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='RF')
        if not tire_rf:
            tire_rf = VehicleTireWidth.objects.filter(vehicle_id = None , type='RF')
        tire_lr = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='LR')
        if not tire_lr:
            tire_lr = VehicleTireWidth.objects.filter(vehicle_id = None , type='LR')
        tire_lf = VehicleTireWidth.objects.filter(vehicle_id = appointment.vehicle.vehicle.id , type='LF')
        if not tire_lf:
            tire_lf = VehicleTireWidth.objects.filter(vehicle_id = None , type='LF')
    else:
        vehicle_parts = VehicleParts.objects.filter(vehicle = None)
        tire_rr = VehicleTireWidth.objects.filter(vehicle = None , type='RR')
        tire_rf = VehicleTireWidth.objects.filter(vehicle_id = None , type='RF')
        tire_lr = VehicleTireWidth.objects.filter(vehicle_id = None , type='LR')
        tire_lf = VehicleTireWidth.objects.filter(vehicle_id = None , type='LF')
        
    
    return render(request, template, {'rr':tire_rr,'rf':tire_rf , 'lr':tire_lr , 'lf':tire_lf , 'tirenote':tirenotes})


def get_walkindata(appointment_id):
    app_details = Appointment.objects.get(id=appointment_id)
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    wlkarnd_details = walkaroundnotes.objects.filter(appointment_id=appointment_id)
    vinimage=None
    odoimage=None
    customer_signatures = None
    if app_details.vehicle.vin_image:
        vinimage= app_details.vehicle.vin_image.url
    if app_details.odometer_image:
        odoimage = app_details.odometer_image.url
    if app_details.customer_signatures:
        sig = app_details.customer_signatures.split(',')
        imgdata = base64.b64decode(sig[1])
        filename = 'cS'+appointment_id+'.png'
        with open(settings.MEDIA_ROOT+'/'+filename, 'wb') as f:
            f.write(imgdata)
            customer_signatures = settings.MEDIA_URL+filename
            
    tires=[]
    other=[]
    service_detail = []
    total_cost = 0
    for obj in app_service:
        sd = {}
        total_cost += obj.service.price
        sd['name'] = obj.service.name
        sd['cost'] = obj.service.price
        sd['note'] = obj.note
        sd['desc'] = obj.desc
        service_detail.append(sd)
    
    for obj in wlkarnd_details:
        temp= {}
        if obj.type == "Tires":
            temp['rr'] = obj.RR.width
            temp['rf'] = obj.RF.width
            temp['lr'] = obj.LR.width
            temp['lf'] = obj.LF.width
            tires.append(temp)
        else:
            temp['type'] = obj.type
            temp['image_name'] = obj.image_name
            temp['notes'] = obj.notes
            if obj.image:
                temp['image'] = obj.image.url
            other.append(temp)
    
    context={"name" : app_details.customer.first_name+" "+ app_details.customer.last_name,
                "cellno" : app_details.customer.phone_number_1,
                "customer_id" : app_details.customer.id,
                "email": app_details.customer.email_1,
                "ccode" : app_details.confirmation_code,
                "aww" : app_details.way_away.name,
                "dealer_name":app_details.dealer.name,
                "vinimage": vinimage,
                "vinreading":app_details.vehicle.vin_number,
                "odoimage": odoimage,
                "odoreading": app_details.odometer_reading,
                "address":app_details.dealer.address_line1+" "+app_details.dealer.address_line2,
                "app_services" : service_detail,
                "tires" : tires,
                "wlkaround": other, 
                "totalcost": total_cost,
                "customer_signatures": customer_signatures,
                "domain": settings.SITE_MAIN_URL
            }
    params = json.dumps(context)
    
    return params


@checkin_access_check
def pfd_view(request,appointment_id):
    template_src= "mobilecheckin/checkin/pdf.html"
    pdf_result = pdf_processing(template_src, appointment_id, request.session["dealer_code"])
    if pdf_result:
        return HttpResponse(pdf_result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors while creating PFD')


def pdf_processing(template_src,appointment_id,dealercode):   
    app_details = Appointment.objects.get(id=appointment_id)
    app_service = AppointmentService.objects.filter(appointment_id = appointment_id)
    total_cost = 0
    for obj in app_service:
        total_cost += obj.price
    wlkarnd_details = walkaroundnotes.objects.filter(appointment_id=appointment_id)
    try:
        dealer =  Dealer.objects.get(dealer_code=dealercode)
    except Exception,e:
        dealer =  None
    context = {'app_details' : app_details,'app_services' : app_service , 'totalcost' : total_cost,
                                      'wlkarnd_details' : wlkarnd_details,'dealer':dealer , 'static': settings.STATIC_ROOT, "domain" : settings.SITE_MAIN_URL}
    template = get_template(template_src)
    html  = template.render(context)
    result = StringIO.StringIO()
    #return render(request, template_src,context )
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result 
    else:
        return None