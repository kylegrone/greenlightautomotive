'''
Created on 27-Nov-2015

@author: Shoaib Anwar
'''
from __builtin__ import True
from base64 import decodestring
import cStringIO
import profile

from PIL import Image
from django.conf import settings
from django.utils import timezone

from customer.services.userservices import CUserService
from dealership.models import Appointment, CustomerVehicle, User, Vehicle, DealersVehicle, VehicleImages, UserProfile, Dealer, \
    VinTrim, WayAway


class VehicleService():
    
    
    def setservices(self):
        from customer.factories import CustomerServicesFactory
        from dealership.factories import DealerShipServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.dealer_service_factory = DealerShipServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        self.userservice = self.dealer_service_factory.get_instance("user")
        self.appointment_service = self.dealer_service_factory.get_instance("appointment")
        self.vehicle_service = self
        self.repair_service = self.dealer_service_factory.get_instance("repair")
        self.dealership_service = self.dealer_service_factory.get_instance("dealership")
    
    
    def save_vehicle_for(self,profile,vehicle):
        try:
            vehicle.user = profile
            vehicle.save()
        except Exception,e:
            print e
            return False
     
    def save_customer_vehicle(self,profile,vehicle_id,vin_number,vehicle_desc=""):
        try:
            vehicle = CustomerVehicle()
            vehicle.vehicle_id = vehicle_id
            vehicle.vin_number = vin_number
            vehicle.user = profile
            vehicle.customer_vehicle_desc = vehicle_desc
            vehicle.save()
            return vehicle
        except Exception,e:
            return None
       
    def save_vehicle_vin_data(self,customer_vehicle,vin_data):
        try:
            if vin_data!=None and vin_data!="":
#                 customer_vehicle.vin_data = vin_data
                filename = str(customer_vehicle.id)+"img.png"
                img  = self.get_img_from_data(vin_data,filename)
                customer_vehicle.vin_image = "./"+filename
#             else:
#                 customer_vehicle.vin_data = ""
#                 customer_vehicle.vin_image = ""
            customer_vehicle.save()
        except Exception,e:
            print e
            return None
        
    def get_img_from_data(self,data,file_name):
        try:
            _, b64data = data.split(',') # [sic]
            b64data = decodestring(b64data)
            tempimg = cStringIO.StringIO(b64data)#.decode('base64'))
            im = Image.open(tempimg)
            im.save(settings.MEDIA_ROOT+"/"+file_name)
            return im
        except Exception,e:
            print e
    def get_vehicle_appointment_detail(self,vehicles,dealer,appointment_obj=None):
        self.setservices()
        vehicles.order_by("vehicle__year__name")
        try:
            vehicles = vehicles.values('id',
                                       'vehicle__make__name',
                                       'vehicle__model__name',
                                       'vehicle__year__name',
                                       'vehicle__mainimage',
                                       'lisence_number',
                                       'vin_number',
                                       'milage','trim_id',
                                       "user__id")
            data = []
            for vehicle in vehicles:
                profile = self.cuserservice.get_user_profile(vehicle["user__id"])
                apt_data = {"is":"false"}
                adv_data = {"is":"false"}
                flag_data = {"is":"false"}
                vehicle["trim__name"] = ""
                profile_data = {"is":"false"}
                
                try:
                    if vehicle["trim_id"] !=None and vehicle["trim_id"] !=0:
                        vehicle["trim__name"] = VinTrim.objects.get(id=vehicle["trim_id"]).name
                except Exception,e:
                    print e
                try:
                    if appointment_obj:   
                        appointment = appointment_obj                        
                    else:               
                        appointment = self.appointment_service.get_active_appointment_by(vehicle["id"],dealer)
                    flag_appointment = self.appointment_service.get_inprogress_appointment_by(vehicle["id"],dealer) 
                    if flag_appointment:     
                        flag_data = {"is":True,"flag_appt_id":flag_appointment.id}      
                        
                    if appointment:
                        servicesrepair = self.appointment_service.get_appointment_services_values(appointment)
                        
                        start_time = ""
                        if appointment.start_time:
                            appointment.start_time = timezone.localtime(appointment.start_time)
                            start_time = appointment.start_time.strftime('%A %b %d, %I:%M %p')
                        
                        apt_data = {"is":"true", 
                                    "time" : start_time,
                                    "code" :appointment.confirmation_code,
                                    "id":appointment.id,
                                    "services":servicesrepair}
                        try:
                            wayaway = WayAway.objects.get(id = appointment.way_away_id)
                            apt_data["wayaway"] = wayaway.name
                        except Exception, ex:
                            pass
                        
                        if appointment.advisor.userprofile.avatar:
                            icon = settings.MEDIA_URL + appointment.advisor.userprofile.avatar.name
                        else:
                            icon = ""
                        adv_data = {"is":"true",
                                    "first" : appointment.advisor.userprofile.first_name,
                                    "last" : appointment.advisor.userprofile.last_name ,
                                    "id" : appointment.advisor_id,
                                    "icon" :  icon}
                    if profile:
                        profile_data = {"is":"true","first_name":profile.first_name,
                                        "last_name":profile.last_name,"id":profile.id}        
                except Exception,e:
                    print "here"
                  
                vehicle["image"] = settings.MEDIA_URL + vehicle["vehicle__mainimage"]#[2:]
                data.append({"vehicle":vehicle, 
                             "appointment":apt_data, 
                             "advisor":adv_data,
                             "profile":profile_data,
                             
                             "flag_data":flag_data})
            return data
        except Exception,e:
            print e
            return []
        
     
     
        
    def get_vehicle_by_confirmation(self,dealer,code):
        data = []
        try: 
            args = ()
            filter_aargs = {
                      "advisor__userprofile__dealer__id" : dealer.id,
                       "confirmation_code" : code
                      }
            appointment = Appointment.objects.get(*args,**filter_aargs
                                                )
            
            print appointment.vehicle.id
            vehicles = CustomerVehicle.objects.filter(id=appointment.vehicle.id)
            data = self.get_vehicle_appointment_detail(vehicles,dealer)
            return data 
        except Exception,e:
            print e
            return []
        
        
    
    def get_vehicle_by_phone(self,dealer,phone):
        self.setservices()
        userservice = self.cuserservice
        data = []
        try: 
            profile = userservice.get_user_profile_by_phone(phone)
            if profile:
                custvehicles = self.get_customer_vehicles_by(profile.id)
                data = self.get_vehicle_appointment_detail(custvehicles,dealer)
            return data 
            
        except Exception,e:
            print e
            return []
        
    def get_detailed_vehicles_by_profile(self,dealer,profile):
        
        self.setservices()
        data = []
        try: 
           
            if profile:
                custvehicles = self.get_customer_vehicles_by(profile.id)
                data = self.get_vehicle_appointment_detail(custvehicles,dealer)
            return data 
            
        except Exception,e:
            print e
            return []
        
        
        
    def get_customer_vehicle(self,vehicle_id):
        try:
            vehicle =  CustomerVehicle.objects.get(id=vehicle_id)
            return vehicle
        except Exception,e:
            None
            
    def get_customer_vehicle_by_model(self,profile,make,model,year):
        try:
            vehicle =  CustomerVehicle.objects.get(user = profile,vehicle__make__name=make,vehicle__model__name=model,vehicle__year__name=year)
            return vehicle
        except Exception,e:
            None
    def check_if_dealer_vehicle(self,vehicle_id,dealer_id):
        try:
            vehicle = DealersVehicle.objects.get(dealer_id = dealer_id,vehicle_id=vehicle_id)
            return True
        except Exception,e:
            return False
    def get_customer_vehicle_by_vin(self,profile,vin):
        try:
            vehicle =  CustomerVehicle.objects.get(user = profile,vin_number=vin)
            return vehicle
        except Exception,e:
            None            
    def delete_customer_vehicle(self,customer_vid):
        """
                thThis method is used to delete customer vehicle
        """
        try:
            custvehicle = CustomerVehicle.objects.get(id = customer_vid)
            if custvehicle:
                custvehicle.delete();
                return True
            return False
        except:
            return False
        
        
    def user_allowed_delete(self,customer_vid,user_id):
        """
            check if the user is allowed to delete the customer vehicle
        """
        try:
            custvehicle = CustomerVehicle.objects.get(id = customer_vid)
            if custvehicle:
                if custvehicle.user_id ==user_id:
                    return True
            return False
        except:
            return False
           
    
    """
    get_vehicle_appointment_data
     * this method is to get the of a vehicle assigned in particular appointment
    """
    def get_vehicle_appointment_data(self , id):        
        self.setservices()
        custvehicle = CustomerVehicle.objects.get(id = id)
        vehicle = Vehicle.objects.get(id = custvehicle.vehicle_id)        
        detail = "%s %s %s" % (vehicle.make.name, vehicle.model.name, vehicle.year.name)
        if custvehicle.color:
            detail += " / "+custvehicle.color
        if custvehicle.lisence_number:
            detail += " / "+custvehicle.lisence_number
       
        data = {'id':id, 
                'detail': detail, 
                'vin': custvehicle.vin_number, 
                'make':vehicle.make.name, 
                'year': vehicle.year.name, 
                'model':vehicle.model.name , 
                'milage' : custvehicle.milage,
                'image' : settings.MEDIA_URL + str(vehicle.mainimage)[2:],
                'lisence':custvehicle.lisence_number}
        return data
    
    
    
    
    def get_customer_vehicles_by(self,profile_id):
        try:
            return CustomerVehicle.objects.filter(user_id = profile_id)
        except:
            return None
        
    
        
        
    def get_customer_vehcile_by_appointment(self,appointment,dealer):
        """
            this method is to get  the vehicles for a customer by appponinmtnet
        """
        self.setservices()
        custvehicles = CustomerVehicle.objects.filter(id = appointment.vehicle.id).all()
        data = self.get_vehicle_appointment_detail(custvehicles, dealer, appointment)
        return data
#      
    
    
    
        
    def get_customer_vehicles(self,user_id,dealer, vehicle_id = None, appointment_id = None):
        """
            this method is to get all the vehicles for a customer
        """
        self.setservices()
        if vehicle_id:
            custvehicles = CustomerVehicle.objects.filter(user_id = user_id, id = vehicle_id).all()
        else:
            custvehicles = CustomerVehicle.objects.filter(user_id = user_id,vehicle_id__in=DealersVehicle.objects.filter(dealer_id=dealer.id).values_list('vehicle_id', flat=True)).all()    
        
        if appointment_id:
            
            appointment = Appointment.objects.get(id = appointment_id)
            data = self.get_vehicle_appointment_detail(custvehicles,dealer, appointment)
            
        else:
            data = self.get_vehicle_appointment_detail(custvehicles,dealer)
       
        return data
    
    
    
    def get_vehichles(self):
#         vehicles = Vehicle.objects .filter(dealer_id=dealer_id)
        vehicles = Vehicle.objects # .filter(dealer_id=dealer_id)
        
        return vehicles.values('id',
                               'make__name',
                               'make__val', 
                               'model__name',
                               'model__val',
                               'year__name',
                               'year__val',
                               'mainimage')
        
        
    def get_vehichles_dealer(self,dealer):
#         vehicles = Vehicle.objects .filter(dealer_id=dealer_id)
        
        vehicles = Vehicle.objects.filter(vehicledealer__dealer_id=dealer.id) # .filter(dealer_id=dealer_id)
        print vehicles
        return vehicles.values('id',
                               'make__name',
                               'make__val',
                                'make__id', 
                               'model__name',
                               'model__val',
                               'model__id',
                               'year__name',
                               'year__val',
                               'year__id',
                               'mainimage')