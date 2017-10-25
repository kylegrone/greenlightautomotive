'''
Created on 27-Nov-2015

@author: Shoaib Anwar
'''
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict

from dealership.models import AppointmentService
from dealership.models import ServiceRepair


class RepairService():
    
    def setservices(self):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.dealer_service_factory = CustomerServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        self.userservice = self.dealer_service_factory.get_instance("user")
        self.appointment_service = self.dealer_service_factory.get_instance("appointment")
        self.vehicle_service = self.dealer_service_factory.get_instance("vehicle")
        self.repair_service = self
        self.dealership_service = self.dealer_service_factory.get_instance("dealership")
        
        
    def get_service_for(self,appointment_id,s_r_type="s"):
        services = AppointmentService.objects.filter(appointment_id = appointment_id,service__type=s_r_type)
        return services 
        
    def get_appointment_services(self, appointment_id):
        services = AppointmentService.objects.filter(appointment_id = appointment_id)
        servicename = ""
        data = []
        if len(services) == 1:
            services = services.get()
            repair = ServiceRepair.objects.get(id = services.service_id)
            servicename =  repair.name
            data.append({'name':servicename, 'id':repair.id, 'type':repair.type , "appt_service_id" : services.id})
        else:
            for ser in services:
                repair = ServiceRepair.objects.get(id = ser.service_id)
                data.append({'name':repair.name, 'id':repair.id, 'type':repair.type, "appt_service_id" : ser.id})
                servicename += repair.name + ", "
            servicename = servicename[:-2]            
        service = {'combined_name':servicename, 'details':data}
        return service
    
    def remove_service (self,id):
        try:
            appt_service = AppointmentService.objects.get(id = id).delete() 
            return True
        except Exception,e:       
            return False
    
    
    
    def get_all_services_for(self,dealer_code,search_text=None):
        
           
        
        services = ServiceRepair.objects.filter(type='s',dealer__dealer_code = dealer_code)
        if search_text:
            try:
                args = (Q(name__contains=search_text) 
                                                        | Q(description__contains=search_text)
                                                        , )
                filter_aargs = {
                          }
                services= services.filter(*args,**filter_aargs)
            except Exception,e:
                print e
        return services
    
    
    
    def get_all_repairs_for(self,dealer_code,search_text=None):
        
        repairs = ServiceRepair.objects.filter(type='r',dealer__dealer_code = dealer_code)
        if search_text:
           
            args = (Q(name__contains=search_text) 
                                                    | Q(description__contains=search_text)
                                                    , )
            filter_aargs = {
                      }
            repairs = repairs.filter(*args,**filter_aargs)
#             repairs.filter(name__contains=search_text)
        return repairs
    
    
    
    def get_all_service_repair_dealer_appt(self, type, dealer_id, appointment_id):
        rservices = ServiceRepair.objects.filter(type=type, dealer__id = dealer_id)
        rservices = rservices.values('id',
                                     'name',
                                     'dms_opcode',
                                     'duration',
                                     'price',
                                     'price_unit',
                                     'image',
                                     'type')
        
        if appointment_id != 0:
            selected_dict = []
            selected_rservices = AppointmentService.objects.filter(appointment_id = appointment_id)
            for selected in selected_rservices:
                selected_dict.append(selected.service_id)
            for index, key in enumerate(rservices):
                
                if rservices[index]["id"] in selected_dict:
                    rservices[index]["selected"] = "true"
                else:
                    rservices[index]["selected"] = "false"
        return rservices
    
    def get_all_services(self):
        services = ServiceRepair.objects.filter(type='s')
        return services
    
    def get_all_repairs(self):
        repairs = ServiceRepair.objects.filter(type='r')
        return repairs
    
    def create_update_appointment_services(self, appt_id , services):
        if services:
            for items in services:
                try:
                    AppointmentService.objects.get(appointment_id = appt_id ,service_id = items )
                except AppointmentService.DoesNotExist:
                    appt = AppointmentService(appointment_id = appt_id , service_id = items)
                    appt.save()
            AppointmentService.objects.filter(appointment_id = appt_id).exclude(service_id__in=services).delete()
        return services
    
    def create_update_delete_appointment_services(self, appt_id , services,s_r_type="s"):
        service_ids_exist = []
        if services:
            for items in services:
                
                try:
                    service = ServiceRepair.objects.get(id=items["service__id"])
                    appt = AppointmentService.objects.get(appointment_id = appt_id ,service_id = items["service__id"] )
                except AppointmentService.DoesNotExist:
                    appt = AppointmentService(appointment_id = appt_id , service_id = items["service__id"])
                
                note = items.get("note","")
                appt.note = note
                appt.price = service.price
                appt.save()
                service_ids_exist.append(items["service__id"])
        self.del_service_ids(appt_id,service_ids_exist,s_r_type)
        return services
    
    def del_service_ids(self,appt_id,service_ids,s_r_type):
        services = AppointmentService.objects.filter(appointment_id=appt_id,service__type=s_r_type).exclude(service_id__in=service_ids)
        if services:
            services.delete()
            
    def create_update_dealer_services(self, data):
        rservices = ServiceRepair()
        if 'id' in data:
            if data['id'] != '0':
                rservices = ServiceRepair.objects.get(id = data['id']) 
            del data['id']
        for k, v in data.iteritems():    
            rservices.__setattr__(k, v)
        rservices.save()        
        return {"id": rservices.pk}
    
    def delete_dealer_services(self, id):
        rservices = ServiceRepair()
        if id != 0:
            rservices = ServiceRepair.objects.get(id = id) 
            rservices.delete()        
        return {"id": id}
    
    def get_service(self, id):
        rservices = ServiceRepair.objects.get(id = id)
        return rservices
    