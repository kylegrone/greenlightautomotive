'''
Created on 17-Nov-2015

@author: Asim Riaz
'''
import code
import datetime
from email.mime.text import MIMEText
import hashlib
import smtplib
import time

from django.conf import settings
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.utils.crypto import get_random_string

from dealership import conf
import dealership
from dealership.models import UserProfile, DriverLiscenseIsurance

from django.core.urlresolvers import reverse


#import dealership
# from dealership import models  as dealership_models
#from dealership.models import CreditCardInfo
class UserService():
    
    def get_profile(self,userprofile_id):
        profile = UserProfile.objects.get(id=userprofile_id)
        return profile
     
    def get_users_for_dealers(self,dealer_id,group_type="Advisor"):
        try:
            techs = User.objects.filter(groups__name=group_type,userprofile__dealer__id=dealer_id)
            return techs
        except Exception,e:
            print e
            return None
    
    
    
    def setservices(self):
        from customer.factories import CustomerServicesFactory
        self.customer_service_factory = CustomerServicesFactory()
        from dealership.factories import DealerShipServicesFactory
        
        self.dealer_service_factory = DealerShipServicesFactory()
        
        self.dealership_service = self.dealer_service_factory.get_instance("dealership")
        self.appointment_service = self
        self.capacity_service = self.dealer_service_factory.get_instance("capacity")
    
        
        
    def check_phone_exist(self,profile,value):
        from dealership.models import  UserProfile
        try:
             
            filter_aargs = {
                      }
            args= ( Q(phone_number_1=value) 
                                                    |Q(phone_number_2=value)
                                                    |Q(phone_number_3=value)
                                                    |Q(active_phone_number=value)
                                                    , )
            
           
            profile_list = UserProfile.objects.filter(*args,**filter_aargs
                                                )
            if profile:
                profile_list= profile_list.exclude(id=profile.id)
            
            return profile_list
        except Exception,e:
            print e
            return None
        
    def check_email_exist(self,profile,value):
        from dealership.models import  UserProfile
        try:
             
            filter_aargs = {
                      }
            args= ( Q(email_1=value) 
                                                    |Q(email_2=value)
                                                    |Q(active_email=value)
                                                   
                                                    , )
            
           
            profile_list = UserProfile.objects.filter(*args,**filter_aargs
                                                )
            if profile:
                profile_list= profile_list.exclude(id=profile.id)
            
            return profile_list
        except Exception,e:
            print e
            return None
        
    def create_guest_account(self, form): 
        response = []
        response['status'] = "success"
        userprofile =  UserProfile() 
        userprofile.first_name = form['first_name']
        userprofile.last_name = form['last_name']
        userprofile.phone_number_1 = form.clean_data['phone_number_1']
        userprofile.email_1 = form.clean_data['email_1']
        try:
            userprofile.save()
        except Exception,e:
            response['status'] = "error"
            print e
            
    def get_dealership(self,user_id):
        "get dealership of a user"
        try:
            user = User.objects.get(id=user_id)
            user_dealer = user.userprofile.dealer
            return user_dealer
        except Exception,e:
            print str(e)
            return None
        
        
    '''Getting username for chat'''
    def get_username_chat(self,request):
        if request.user.is_authenticated():
            return request.user.username
        else:
            if "guest_id" in request.session:
                return request.session["guest_id"]
            else:
                request.session["guest_id"] = "GUEST"+get_random_string()
                return request.session["guest_id"]
            
            
            
    '''Getting Nick name of user for Chat'''
    def get_chatnick(self,request):
        if request.user.is_authenticated():
            return request.user.username
        else:
            return "Guest"
        
    def save_user_pasword_answers(self,user,password,question,answer):
           
            user.set_password(password)
            if hasattr(user,"userprofile") == False:
                user.userprofile = dealership.models.UserProfile()
            user.userprofile.question = question
            user.userprofile.answer =  answer
            user.userprofile.save()
            user.save()
        
    def save_user_password(self, user, password):
        user.set_password(password)
        user.save()
        self.delete_token(user)   
        
    def get_user_name(self, id): 
        try:
            user = User.objects.get(id = id) 
            if user.userprofile:     
                return "%s %s" % (user.userprofile.first_name, user.userprofile.last_name)  
            else:
                return "%s %s" % (user.first_name, user.last_name)
        except Exception, e:
            return ""           
      
    def create_token(self, user):
        userprofile = dealership.models.UserProfile.objects.get(user=user)
        m = hashlib.md5()
        m.update(str(user.id) + user.username + str(time.time()))
        token = m.hexdigest() 
        EndDate = datetime.datetime.now() + datetime.timedelta(days=3)
        userprofile.token = token
        userprofile.token_expiry = EndDate
        userprofile.save()
        return token
    
    def delete_token(self, user):
        if user.userprofile:
            user.userprofile.token = None
            user.userprofile.token_expiry = None
            user.userprofile.save()
        
    def send_pass_reset_link(self, user, request, path):           
        link = conf.PROTOCOL + settings.SITE_MAIN_URL + path + '?token='+self.create_token(user)
        print link       
        msg = "recover you password using this link \n" +  link 
        send_mail('Password Reset', msg , settings.DEFAULT_EMAIL_FROM , [user.email] , fail_silently=False)
        
    def send_pass_reset_link_new(self, user, request, path,email,dealer_code):           
        link = settings.SITE_MAIN_URL + path + '?token='+self.create_token(user)+"&dealer_code="+dealer_code
               
        msg = "recover you password using this link \n" +  link 
        send_mail('Password Reset', msg , settings.DEFAULT_EMAIL_FROM , [email] , fail_silently=False)
        
            
    def send_username_link(self, user):
        msg = "your username is : " + user.username     
        send_mail('Username', msg , settings.DEFAULT_EMAIL_FROM , [user.email] , fail_silently=False)  
        
    def send_username_link_new(self, user,email):
        msg = "Your username is : " + user.username     
        send_mail('Username', msg , settings.DEFAULT_EMAIL_FROM , [email] , fail_silently=False) 
        
    def send_account_request(self, email):
        msg = "Please create a Dealership account using this email ID : " + email     
        send_mail('Account Request', msg , settings.DEFAULT_EMAIL_FROM , [conf.ADMIN_EMAIL] , fail_silently=False)     
        
    def get_user_from_token(self, token):
        try:
            profile = dealership.models.UserProfile.objects.get(token = token)
        except:
            return None   
        if profile.token_expiry > datetime.datetime.now().date():
            user = User.objects.get(id=profile.user_id)
            return user
        return None 
    
    def get_user_question(self, user):
        question = dealership.models.Questions.objects.get(id = user.userprofile.question_id)
        return question.question_text
    
    def verify_user_answer(self, user, answer):
        if user.userprofile.answer == answer:
            return True
        return False
    
    def sendEmailPDf(self,email,text):
        msg = "Please find your action plan at given link" + text
        send_mail('Action Plan', email  , settings.DEFAULT_EMAIL_FROM , email  , fail_silently=False)
    def sendEmail(self,emailAddress,text):
#         s = smtplib.SMTP(conf.SMTP_ADDRESS)
#         s.sendmail(conf.SENDER_EMAIL, emailAddress, text)    
#         s.quit()
        msg = "Please create a Dealership account using this email ID : " + emailAddress     
        send_mail('Account Request', emailAddress  , settings.DEFAULT_EMAIL_FROM , emailAddress  , fail_silently=False)     
            
            
            
    def sendEmailToITForCreation(self,newUserEmail):
        users = User.objects.filter(groups__name__in = ['IT'])
        for user in users:
            self.sendEmail(user.email,newUserEmail + "has requested to Join")
   
    def get_dealers_advisors(self, dealer, datetime_string=None):
        advisors = User.objects.filter(groups__name__in = ['Advisor'], userprofile__dealer = int(dealer))   
        
        data = []
        for adv in advisors:
            data.append({'id':adv.id, 'title':"%s %s" % (adv.userprofile.first_name, adv.userprofile.last_name) , 'size':1, 'capacity':2}) 
        return data 
        #{'data':data}


    def get_insurance_detail(self, id):
        instance = DriverLiscenseIsurance.objects.get(id=id)
        return instance
    
    def get_customer_detail(self, id):
        user = UserProfile.objects.get(id = id) 
        #customer = model_to_dict(user)
        credit_card = 0
        try:
            credit_card = user.cc_profile.card_number[-4:] 
        except Exception, ex:
            pass
        
        insurance = []
        try:
            insurance = user.insuranceprofile 
        except Exception, ex:
            pass
        
        customer = {
                    'id': user.id,
                    'name':"%s %s" % (user.first_name, user.last_name),
                    'active_phone_number':user.active_phone_number,
                    'active_email':user.active_email,
                    'email_1':user.email_1,
                    'method_of_contact': user.method_of_contact,
                     user.phone_1_type : user.phone_number_1,
                     user.phone_2_type : user.phone_number_2,
                     user.phone_3_type : user.phone_number_3,
                    'address_line1': user.address_line1,
                    'address_line2': user.address_line2,
                    'customer_notes': user.customer_notes,
                    'insurance' : insurance,
                    'cc':credit_card
                   }  
    
            

 
        return customer  
    
    def send_registration_link(self, request, customer_id):   
        register_link = "%s?dealer_code=%s&profile_id=%s" % (reverse('customer:registeruer'), 
                                                             request.session["dealer_code"],
                                                             customer_id)        
        link = conf.PROTOCOL + settings.SITE_MAIN_URL + register_link   
        msg = "Please create your profile using this link \n" +  link 
        send_mail('Create Profile', msg , settings.DEFAULT_EMAIL_FROM , [request.POST.get("email_1")] , fail_silently=False)
