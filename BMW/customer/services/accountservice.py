from django.contrib import messages
from customer.services.userservices import CUserService
from dealership.services.userservices import UserService


class AccountService():
    
    
        
        
    def setservices(self):
        from customer.factories import CustomerServicesFactory
        from dealership.factories import DealerShipServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.dealer_service_factory = DealerShipServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        self.userservice = self.dealer_service_factory.get_instance("user")        
        
        
          
    def create_emptyuser(self,user):
        try:
            pass
        except Exception:
            pass
        
        
    def check_profile_by_phone(self,user):
        pass
    
    
    def delete_account(self,profile):
        """
               THis method is used to delete all the account related information for 
               the userprofie
        """
        try:
#             service = CUserService()
            self.setservices()
            
            self.cuserservice.empty_userprofile(profile)
            self.cuserservice.del_cc_profile(profile)
            self.cuserservice.del_user_driver_insurance(profile)
            return True
        except Exception,e:
            print e
            return False
        
        
    def save_driver_form(self,insurance_profile,driver_form ):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        if driver_form.is_valid():
            try:
                state= driver_form.cleaned_data["state_us"]
                driver_form.save()
                if self.cuserservice.set_insurance_state(insurance_profile,state)== False:
                    raise Exception("Unable to save state")
                    
                
                return True
            except Exception as e:
                driver_form.add_error(None,str(e))
                return False
        else:
            return False
            
    def save_cc_form(self,insurance_profile,cc_form ):
        if cc_form.is_valid():
            try:
                cc_form.save()
                return True
            except Exception as e:
                cc_form.add_error(None,str(e))
                return False
        else:
            return False
        
    def save_password_form(self,pass_form,user):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
#         userservice = UserService()
        if pass_form.is_valid():
            try:
                if user.check_password(pass_form.cleaned_data['current']) == True:
                    self.cuserservice.save_user_password(user, pass_form.cleaned_data['new'])
                    return True
                else:
                    pass_form.add_error("current","Current password not correct") 
                    return False
            except Exception as e:
                pass_form.add_error(None,str(e))
                return False
        else:
            return False
           
    def save_account_form(self,user,userprofile,customer_form,account_initial ):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        
        if customer_form.is_valid():
            try:
                first_name = customer_form.cleaned_data["first_name"]
                last_name = customer_form.cleaned_data["last_name"]
                state= customer_form.cleaned_data["state_us"]
                if user:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save() 
                customer_form.save()
                self.cuserservice.set_user_state(userprofile,state)
               
                return True
            except Exception as e:
                customer_form.add_error(None,str(e))
                return False
        else:
            
            return False
                        
        
    def get_initial_cc_form(self,user,insurance_profile,userprofile):
        
        first_name = insurance_profile.first_name
        last_name = insurance_profile.last_name
        if insurance_profile.first_name == "":
            first_name = userprofile.first_name
        if insurance_profile.last_name == "":
            last_name = userprofile.last_name
        initial = {"first_name":first_name,"last_name":last_name,"user":userprofile.id
                   }
        return initial  
       
    def get_initial_driver_form(self,user,insurance_profile,userprofile):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        state = self.cuserservice.get_insurance_state(insurance_profile)
        initial = {"state_us":state,"user":userprofile.id
                   }
        return initial
    #     return CustomerInsuranceForm(initial=initial,instance=insurance_profile)    
    
            
    def get_initial_user_form(self,user,userprofile ):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        self.cuserservice = self.customer_service_factory.get_instance("user")
        state = self.cuserservice.get_user_state(userprofile)
        country = "US"
        if userprofile.country!="":
            country =userprofile.country
        initial = {"state_us":state,"user":user.id,"first_name":userprofile.first_name,"last_name":userprofile.last_name,
                   "country":country
                   }
        return initial
    
    