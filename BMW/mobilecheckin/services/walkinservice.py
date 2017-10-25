from dealership.models import *
from django.db.models import Q
import datetime






class WalkinService():
    
    
    
    def get_slab(self,now,open_time,close_time):
        
        slab_first =  open_time
        slab_second =  open_time + datetime.timedelta(minutes = 20)
        while slab_second <= close_time:
            appt = Appointment.objects.filter(start_time__range=[slab_first,slab_second]).count()
            if appt < 4:
                return slab_first
                break
            slab_first =  slab_first + datetime.timedelta(minutes = 20)
            slab_second = slab_second + datetime.timedelta(minutes = 20)
            
        return None
    
    
    
    def search_customer(self,phonenumber):
        user =UserProfile.objects.filter(Q(phone_number_1=phonenumber) | Q(phone_number_2=phonenumber))
        
        return user
    
    def customer_vehicles(self,user):
        c_veh = CustomerVehicle.objects.filter(user_id = user.id)
        vehicles = []
        if c_veh:
            for obj in c_veh:
                dict = {}
                dict['name'] = obj.vehicle.make.name+" "+obj.vehicle.model.name+" "+obj.vehicle.year.name
                dict['id'] = obj.vehicle.id
                dict['vin'] = obj.vin_number
                dict['make_val'] = obj.vehicle.make.val
                dict['model_val']=obj.vehicle.model.val
                dict['year_val']=obj.vehicle.year.val
                vehicles.append(dict)
        return vehicles