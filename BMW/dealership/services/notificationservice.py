from cgitb import text
import email

from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives
from django.template.context import Context
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.utils.text import phone2numeric
import phonenumbers

from BMW import settings
from dealership.models import ReminderSettings, EmailTypes
from dealership.services.emailservice import EmailService
from dealership.services.twilio_service import TwillioService


class NotificationService():
    
    REMINDER_TYPES = (1,2,3,4)
    
    SCHEDULE_APPOINTMENT_TYPE = 1
    FLAGGING_APPOINTMENT_TYPE = 4
    frm_text= TwillioService.default_number
    def send_dealer_based_notification(self,dealer,profile,context,email_type,send_email=True,send_text=False,attachment=None):
        try:
            
            frm = dealer.from_email
            email = profile.active_email
#             email = "asimriaz85@gmail.com"
            if email==None or email =="":
                email = profile.email_1
            if email and (send_email == True ):
                try:
                    emailtype = EmailTypes.objects.get(name=email_type,dealer_id=dealer.id)
                except Exception,e:
                    emailtype = None
                if emailtype:
                    emailservice = EmailService()
                    subject = emailtype.subject
                    date_time = timezone.now()
                    emailservice.savequeue(frm , email, date_time , "", "" , emailtype , subject , context,dealer.id,attachment)
            
            if send_text == True:
                        self.send_text_notification(profile,emailtype,context)
            
            return True    
        except Exception,e:
            print "error sending notification"
            print e
            return False
        
    def send_notification(self,profile,frm,template_email,template_text,subject,context,frm_text=None,send_email=True,send_text=False):
        try:
            
            email = profile.active_email
            if email==None or email =="":
                email = profile.email_1
            if email and (send_email == True ):
                self.send_email(template_email, context, email, frm, subject)
            phone_number = profile.active_phone_number
            if phone_number== None :
                phone_number =profile.phone_number_1
            if phone_number and send_text:
                self.send_text(template_text,context,phone_number,self.frm_text)
            
            return True    
        except Exception,e:
            print "error sending notification"
            print e
            return False
        
        
    def send_text_notification(self,profile,emailobj,context):
        phone_number = profile.active_phone_number
        template ='text/'+emailobj.template
        if phone_number== None :
            phone_number =profile.phone_number_1
        if phone_number:
            self.send_text(template,context,phone_number,self.frm_text)

    def get_schedlued_settings(self,profile):
        try:
            settings = self.get_user_remindersettings_for(self.SCHEDULE_APPOINTMENT_TYPE,profile)
            return {"text":settings.text,"email":settings.email,"phone":settings.phone}
        except Exception,e:
            print e
            return {"text":False,"email":False,"phone":False}
            
            
            
    def get_flagging_settings(self,profile):
           
        try:
            settings = self.get_user_remindersettings_for(self.FLAGGING_APPOINTMENT_TYPE,profile)
            return {"text":settings.text,"email":settings.email,"phone":settings.phone}
        except Exception,e:
            print e
            return {"text":True,"email":True,"phone":True}
            
    def convert_to_e164(self,raw_phone):
        if not raw_phone:
            return
    
        if raw_phone[0] == '+':
            # Phone number may already be in E.164 format.
            parse_type = None
        else:
            # If no country code information present, assume it's a US number
            parse_type = "US"
    
        phone_representation = phonenumbers.parse(raw_phone, parse_type)
        return phonenumbers.format_number(phone_representation,
            phonenumbers.PhoneNumberFormat.E164)        
        
        
    def send_text(self,template,context,to,frm):
        try:
            twilio = TwillioService()
            to = str(to)
#             to = self.convert_to_e164(to)
            if to.startswith("+")==False:
                to = "+"+to
                
                
            msg_plain = render_to_string(template,context)
#             msg_html = render_to_string(template, context)
            twilio.send_message(msg_plain, to, frm)
#             send_mail(subject, msg_plain , settings.EMAIL_HOST_USER , [to] ,html_message=msg_html, fail_silently=False)
      
            print "message sent"
        except Exception,e:
            print "error sending text"
            print e
            return False
    
    
    def send_email(self,template,context,to,frm,subject):
        try:
           
            msg_plain = render_to_string(template,context)
            msg_html = render_to_string(template, context)

            send_mail(subject, msg_plain , settings.EMAIL_HOST_USER , [to] ,html_message=msg_html, fail_silently=False)
        except Exception,e:
            print "error sending email"
            print e
            return False
    
    def save_reminder_settings(self,id,email,text,phone):
        try:
            reminder =ReminderSettings.objects.get(id=id)
            reminder.email = email
            reminder.text   = text
            reminder.phone = phone
            reminder.save()
            return True 
        except Exception,e:
            print "erererer"
            print e
            return False
    
    
    
    def get_user_remindersettings(self,profile,create_if_not=False):
        try:
            reminders = ReminderSettings.objects.filter(type_id__in = self.REMINDER_TYPES,customer_id=profile.id)
            if (reminders == False or len(reminders) <4) and create_if_not:
                return self.create_reminders_default(profile)
            return reminders       
        except Exception,e:
            print e
            return None
        
    
    def get_user_remindersettings_for(self,reminder_type_id,profile):
        try:
            reminder = ReminderSettings.objects.get(type_id = reminder_type_id,customer_id = profile.id)
            return reminder
        except Exception,e:
            return None
        
    def create_reminders_default(self,profile):
        for reminder in self.REMINDER_TYPES:
                    self.create_reminder_setting_for(reminder, profile)
        return self.get_user_remindersettings(profile)        
    
    
        
    def create_reminder_setting_for(self,reminder_type_id,profile):
        try:
            reminder = ReminderSettings.objects.get(type_id = reminder_type_id,customer_id = profile.id)
            return reminder
        except Exception,e:
            print e
            reminder = ReminderSettings()
            reminder.type_id = reminder_type_id
            reminder.customer = profile
            reminder.save()
            return reminder
    
    
            