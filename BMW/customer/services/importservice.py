
import csv
from datetime import datetime
import os

from django.contrib.auth.models import User

from customer.services.userservices import CUserService
from dealership.models import UserProfile, CustomerVehicle, Appointment, \
    AppointmentRecommendation, RO, Notes, AppointmentService
from dealership.services.vehicleservices import VehicleService


class ImportContact():
    
    current_profile = None
    current_appointment =None
    current_vehcile=None
    userservice = CUserService()
    vehicleservice = VehicleService()
    dealer_id = 2
    advisor1=146
    advisor2=180
    
    
    def import_file(self,file_name="infiiniti.csv"):
        pass
#         module_dir = os.path.dirname(__file__)  # get current directory
#         file_path = os.path.join(module_dir, '../../'+file_name)
#         file  = open(file_path,"r+")
#         reader = csv.reader(file)
#         line_count = 0
#         
#         for row in reader:
#             if line_count >1:
#                 self.add_row(row)
#             if line_count > 1000:
#                 break
#             line_count = line_count +1
#         file.close()
        
    def add_row(self,row):
        

        
        first_name = row[1]
        last_name = row[2]
        email = row[3]
        phone_2 = "".join(i for i in row[4] if i.isdigit())
        phone_1 = "".join(i for i in row[5] if i.isdigit())
        country = row[6]
        address = row[7]
        city = row[8]
        state = row[9]
        zip_code = row[10]
        year = row[18]
        make = row[19]
        model = row[20]
        vin = row[26]
        vin = row[26]
        color = row[28]
        mileage = row[29]
        appt_time = row[33]
        appt_creation_time = row[34]
        advisor = row[35]
        service = row[41]
        price =row[44] 
        price = price.replace("$","")
#         price = "".join(i for i in row[44] if i.isdigit())
        
            
        try:
            price = float(price)
        except Exception,e:
            print e
            price = 0.00
        status = row[45]
        
      
        self.current_profile = self.getCustomer(first_name, last_name, email, phone_1, phone_2, country, address, city, state, zip_code)
        if self.current_profile:
            self.current_vehcile  = self.getVehicle(make, model, year, vin,color,mileage)
            if  self.current_vehcile !=None:
                self.current_advisor = self.getAdvisor(self.advisor1)
                self.current_appointment = self.getAppointment(appt_time,appt_creation_time,status)
                if  self.current_appointment:
                    self.add_service(service,price,status)
            
            
    def getCustomer(self,first_name,last_name,email,phone_number1,phone_number2,country,address,city,state,zip_code):
        if first_name==None or last_name==None or first_name.strip()=="" or last_name.strip()=="" or email.strip()=="":
            if self.current_profile !=None:
                return self.current_profile
        elif email!=None and email.strip()!="":
            email = email.lower()
            tmp_customer = self.checkCustomer(email)
            print tmp_customer
            if not tmp_customer :
                self.current_profile = self.createCustomer(first_name,last_name,email,phone_number1,phone_number2,country,address,city,state,zip_code)
            else:
                self.current_profile = tmp_customer
            return self.current_profile
            
        return False
    
    def createCustomer(self,first_name,last_name,email,phone_number1,phone_number2,country,address,city,state,zip_code):

        
        username = email.split("@")
        username[0] = username[0]+"_infiniti"
        user = self.userservice.create_customer(username[0])
#         user.username = username[0]
        
        user.email = email
        user.save()
        user.set_password("Password1")
        user.save()
        userprofile = UserProfile()
        userprofile.user =user
        userprofile.first_name = first_name
        userprofile.last_name = last_name
        userprofile.email_1 = email
        userprofile.phone_number_1 = phone_number1
        userprofile.phone_number_2 = phone_number2
        userprofile.country = "US"
        userprofile.zipcode = zip_code
        userprofile.city = city
        userprofile.address_line1 = address
        userprofile.save()
        return userprofile
        
    def checkCustomer(self,email):
        profile = self.userservice.get_user_profile_by_email(email)
        if profile:
            return profile
    
    def getVehicle(self,make,model,year,vin,color,mileage):
        if make==None or make.strip()=="" or model==None or model.strip()=="":
            if self.current_vehcile !=None:
                return self.current_vehcile
        else:
            customer_vehicle = self.vehicleservice.get_customer_vehicle_by_vin(self.current_profile,vin)
            if not customer_vehicle:
                customer_vehicle = self.vehicleservice.get_customer_vehicle_by_model(self.current_profile,make,model,year)
                if customer_vehicle and self.vehicleservice.check_if_dealer_vehicle(customer_vehicle.vehicle_id,self.dealer_id) == False:
                    customer_vehicle  = False
            if not customer_vehicle:
                customer_vehicle = CustomerVehicle()
                customer_vehicle.vehicle_id = 1166
                customer_vehicle.user = self.current_profile
                customer_vehicle.customer_vehicle_desc = make+"/"+model+"/"+year
                customer_vehicle.vin_number = vin
                customer_vehicle.mileage = mileage 
                customer_vehicle.save()
            return customer_vehicle
    
    
            
    
    
    def add_service(self,service_note,price,status="Completed"):
        try:
            app_service = AppointmentService()
            app_service.service_id = 92
            app_service.appointment = self.current_appointment
            app_service.note = service_note.decode('utf-8', 'ignore')
            app_service.price = price
            app_service.save()
#             recommendations = AppointmentRecommendation()
#             recommendations.appointment = self.current_appointment
#             recommendations.price = price
#             recommendations.price_unit = "$"
#             recommendations.notes = service.decode('utf-8', 'ignore')
#             if self.current_appointment.appointment_status_id == 8:
#                 recommendations.status = "Accept"
#                 recommendations.result = "Success"
#             recommendations.save() 
        except Exception,e:
            print e
            raise Exception(e)
        
        
        
    def getAppointment(self,appointment_time,appt_creation_time,status="Completed"):
        if appointment_time !=None and appointment_time.strip()!="":
            appointment = Appointment()
            ro = RO()
            try:
#                 06/01/2016 10:40 AM
                appt_creation_time = appt_creation_time.upper()
                start_time = datetime.strptime(appt_creation_time.strip(),"%m/%d/%Y %I:%M %p")
            except Exception,e:
                start_time = datetime.strptime("06/01/2016 10:40 AM","%m/%d/%Y %I:%M %p")
            try:
#                 06/01/2016 10:40 AM
                appointment_time = appointment_time.upper()
                end_time = datetime.strptime(appointment_time.strip(),"%m/%d/%Y %I:%M %p")
                
            except Exception,e:
                end_time =start_time  #datetime.strptime("06/01/2016 11:40 AM","%m/%d/%Y %I:%M %p")
            appointment.start_time = start_time
            appointment.end_time = end_time
            appointment.appointment_status_id = 11
            appointment.customer_id = self.current_profile.id
            appointment.advisor = self.current_advisor.user
            appointment.vehicle_id = self.current_vehcile.id
            appointment.dealer_id = self.dealer_id
            appointment.comments = "Added by import tool"
            appointment.save()
            ro.ro_number = appointment.id
            ro.rfid_tag = appointment.id
            ro.ro_date = appointment.start_time
            ro.ro_status =0
            if status.lower().strip() == "completed" or status.lower().strip() =="arrived" or status.lower().strip() =="":
                appointment.appointment_status_id = 8
                ro.flag1_id = 71
                ro.flag2_id = 74
                ro.flag3_id = 39
                ro.ro_status = 1
                ro.inspection_status = "Completed"
            ro.save()
            appointment.ro = ro
            appointment.save()
            return appointment
        else:
            if self.current_appointment!=None:
                return self.current_appointment
            return False
        return False
    
    def getAdvisor(self,profile_id):
        userprofile = UserProfile.objects.get(id = profile_id)
        return userprofile
    
    
    def addServices(self,appointment,note,price):
        pass
    
    def setAppointment(self,appointment,status):
        pass