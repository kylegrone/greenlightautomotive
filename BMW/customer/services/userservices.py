

from datetime import  datetime

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models.fields import NOT_PROVIDED
from django.db.models.query_utils import Q
from django.utils.text import phone2numeric

from customer.app_confg import confg
from dealership.conf import DEALER_ID
from dealership.models import UserProfile, DriverLiscenseIsurance, \
    CreditCardInfo, Appointment, CustomerAdvisor
from dealership.services.userservices import UserService
from livechat.forms import UploadForm


class CUserService(UserService):
     
    def save_special_offer_notify(self,profile,special):
        try:
            profile.special_offer_notify = special
            profile.save()
        except Exception,e:
            print e
            return False 
        
        
    def save_active_phone(self,profile,phone,carrier_choice=None):
        try:
            profile.active_phone_number = phone
            profile.active_phone_number_date = datetime.now()
            if carrier_choice:
                profile.carrier_choices = carrier_choice
            profile.save()
        except Exception,e:
            print e
            return False 
        
    def save_active_email(self,profile,email):
        try:
            profile.active_email = email
            profile.active_email_date = datetime.now()
            profile.save()
        except Exception,e:
            print e
            return False 
        
        
    def create_customer(self,username):
        try:
            user = User()
            user.username = username
            
            user.save()
            g = Group.objects.get(name=confg.GROUP_NAME) 
            g.user_set.add(user)
            return user 
        except Exception,e:
            print e
            return False
    
    def get_my_advisor(self,profile_id,dealer_id):
        try:
            myadvisor = CustomerAdvisor.objects.get(customer_id=profile_id,dealer_id=dealer_id)
            return myadvisor.advisor
        except:
            return None
        
    def get_advisor_for_chat(self,dealership,profile):
        advisor = None
        try:
            if profile:
                advisor = self.get_my_advisor(profile.id,dealership.id)
            if advisor ==None:
                advisors = User.objects.filter(groups__name=confg.ADVISOR_GROUP_NAME,userprofile__dealer__id=dealership.id,userprofile__available_for_chat=True).order_by('userprofile__number_of_chats').all()[:1]
                advisor = advisors[0]
            
            return advisor
        except:
            return None    
        return advisor
       
    def save_my_advisor(self,profile_id,dealer_id,advisor_id):
        try:
            myadvisor = CustomerAdvisor.objects.get(customer_id=profile_id,dealer_id=dealer_id)
        except:
            myadvisor = CustomerAdvisor()
        myadvisor.customer_id = profile_id
        myadvisor.dealer_id = dealer_id
        myadvisor.advisor_id = advisor_id
        myadvisor.save()
        return True
        
        
        
    def get_user_profile_by_phone(self,phone):
        try:
            
            filter_aargs = {} 
            args= ( Q(active_phone_number=phone) 
                                                    |Q(phone_number_1=phone)
                                                    |Q(phone_number_2=phone)
                                                    |Q(phone_number_3=phone), )
            
                
            
            profile = UserProfile.objects.get(*args,**filter_aargs
                                                )
            return profile
        except:
            return None
        
    def get_user_profile_by_email(self,email):
        try:
            filter_aargs = {} 
            args= ( Q(active_email=email) 
                                                    |Q(email_1=email)
                                                    |Q(email_2=email)
                                                    , )
            profile = UserProfile.objects.get(*args,**filter_aargs
                                                )
            return profile
        except:
            return None 
        
    
    def get_user_profile(self,profile_id):
        try:
                profile = UserProfile.objects.get(id = profile_id)
                return profile
        except Exception:
            return None
            
            
    def get_all_advisor_for(self,dealer_code):
        try:
            return   User.objects.filter(groups__name__in = ['Advisor'], userprofile__dealer__dealer_code = dealer_code)
        except:
            return None
        
        
     
     
        
    def get_all_available_advisor_for(self,dealer_code,appointment=None):
        self.setservices()
        dealer = self.dealership_service.get_dealer_by(dealer_code)
        
        try:
                advisors = []
                users = User.objects.filter(groups__name__in = ['Advisor'], userprofile__dealer = dealer)
                for user in users:
                    tmp_user = {"id":user.id,"profile":user.userprofile.id,"first_name":user.userprofile.first_name,
                                "last_name":user.userprofile.last_name,
                                "userprofile__avatar":user.userprofile.avatar.name}
                    if appointment and appointment.start_time:
                        if self.capacity_service.check_slab_for_advisor(dealer,appointment.start_time,user,appointment):
                            advisors.append(tmp_user)
                    else:
                            advisors.append(tmp_user)
               
                return advisors
        except Exception,e:
            print e
            return []
        
        
    def get_all_available_advisor_for_slab_time(self,dealer_code,slab_time):
        self.setservices()
        dealer = self.dealership_service.get_dealer_by(dealer_code)
        
        try:
                advisors = []
                users = User.objects.filter(groups__name__in = ['Advisor'], userprofile__dealer = dealer)
                for user in users:
                    tmp_user = {"id":user.id,"profile":user.userprofile.id,"first_name":user.userprofile.first_name,
                                "last_name":user.userprofile.last_name,
                                "userprofile__avatar":user.userprofile.avatar.name}
                    
                    if self.capacity_service.check_slab_for_advisor(dealer,slab_time,user,None):
                            advisors.append(tmp_user)
                    else:
                            advisors.append(tmp_user)
               
                return advisors
        except Exception,e:
            print e
            return []
     
     
     
           
        
    def set_centrifuge_context(self,request,dealer_code,profile,context={},chatposition="bottom"):
        self.setservices()
        dealer = self.dealership_service.get_dealer_by(dealer_code)
        advisor = self.get_advisor_for_chat(dealer,profile)
       
        img=UploadForm()
        chat_username = self.get_username_chat(request)
        chat_nick = self.get_chatnick(request)
        context_centrifuge = {"CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
                                          "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET,
                                          "chatadvisor":advisor,"chat_username":chat_username,"chat_nick":chat_nick
                                         ,'imgform':img,"chatposition":chatposition}
        context.update(context_centrifuge)
        
        
    def send_pass_reset_link(self, user, token):
        msg = "recover http://localhost:8000/customer/password/create?token="+token                    
        send_mail('passwordreset', msg , settings.DEFAULT_EMAIL_FROM,[user.email], fail_silently=False) 
        
    def send_pass_reset_link_profile(self, profile, token,email,dealer_code):
#         msg = "recover "+settings.customer/password/create?token="+token          
        msg = "recover "+settings.SITE_MAIN_URL+reverse('customer:passcreate')+"?token="+token+"&dealer_code=" +dealer_code        
        send_mail('passwordreset', msg , settings.DEFAULT_EMAIL_FROM,[email], fail_silently=False)
        
      
        
    def send_username_link(self, user):
        msg = "username : "+user.username              
        send_mail('Username', msg , settings.DEFAULT_EMAIL_FROM,[user.email], fail_silently=False)
    
    
    def send_username_link_profile(self, user,email):
        msg = "Username is : "+user.username              
        send_mail('Username', msg , settings.DEFAULT_EMAIL_FROM,[email], fail_silently=False)
    
            
    def get_userprofile(self,user):
        user = User.objects.get(id=user.id)
        
        try:
            if user.userprofile:
                return user.userprofile
            else:
                user.userprofile = UserProfile()
                user.userprofile.save()
        except:
            user.userprofile = UserProfile()
            user.userprofile.save()
        return user.userprofile
    
    
    def empty_userprofile(self,profile):
        try:
            if profile:
                for f in profile._meta.fields:
                    if f.default <> NOT_PROVIDED:
                        setattr(profile, f.name, f.default)
            return True
        except Exception,e:
            print e
            return False
        
        
    def del_userprofile(self,user):
        try:
            if user.userprofile:
                user.userprofile.delete()
            return True
        except:
            return False
    
    def get_user_driver_insurance(self,profile):
        try:
            if profile.insuranceprofile:
                return profile.insuranceprofile
            else:
                profile.insuranceprofile = DriverLiscenseIsurance()
                profile.insuranceprofile.save()
        except:
            profile.insuranceprofile = DriverLiscenseIsurance()
            profile.insuranceprofile.save()
        return profile.insuranceprofile
    
    def del_user_driver_insurance(self,profile):
        try:
            if profile.insuranceprofile:
                profile.insuranceprofile.delete()
            return True
        except:
            return False
    
    def get_cc_profile(self,profile):
        try:
            if profile.cc_profile:
                return profile.cc_profile
            else:
                profile.cc_profile = CreditCardInfo()
                profile.cc_profile.save()
        except:
            profile.cc_profile = CreditCardInfo()
            profile.cc_profile.save()
        return profile.cc_profile
    
    
    def del_cc_profile(self,profile):
        try:
            if profile.cc_profile:
                profile.cc_profile.delete()
                return True
           
        except:
            return False
        
    def get_user_state(self,userprofile):
        try:
            return userprofile.state_us
        except:
            None
            
   
    def set_user_state(self,userprofile,state):
        try:
            userprofile.state_us = state
            userprofile.save()
            return True
        except:
            return False
        
    def get_insurance_state(self,insurance_profile):
        try:
            return insurance_profile.state
        except:
            None
           
    def set_insurance_state(self,insurance_profile,state):
        try:
            insurance_profile.state = state
            insurance_profile.save()
            return True
        except:
            return False
        
    def get_profile_numbers(self,profile):
        try:
            phone = []
            if profile.phone_1_type == "Mobile" and profile.phone_number_1!=""  and profile.phone_number_1!=None  and profile.phone_number_1!=0:
                phone.append(profile.phone_number_1) 
            if profile.phone_2_type == "Mobile" and profile.phone_number_2!="" and profile.phone_number_2!=None  and profile.phone_number_2!=0:
#                 phone[1] = profile.phone_number_2
                phone.append(profile.phone_number_2)
                
            if profile.phone_3_type == "Mobile" and profile.phone_number_3!="" and profile.phone_number_3!=None  and profile.phone_number_3!=0:
#                 phone[3] = profile.phone_number_3
                phone.append(profile.phone_number_3)
            
            return phone
        except Exception,e:
            print e
            return []
        
    def get_profile_emails(self,profile):
        try:
            email = []
            if profile.email_1 != "" and profile.email_1!=None :
                email.append(profile.email_1)
            if profile.email_2 != "" and profile.email_1!=None:
                email.append(profile.email_2)
                
            return email
        except Exception,e:
            print e
            return []