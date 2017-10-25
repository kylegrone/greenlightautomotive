'''
Created on 17-Nov-2015

@author: Shoaib Anwar
'''

from datetime import datetime
import json
import os
from email.mime.image import MIMEImage
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives
from django.template import Context
from django.template.base import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone

from django.conf import settings

from dealership.models import *


class EmailService():
    IN_QUEUE_STATUS = 1
    PENDING_STATUS = 0
    SENT_STATUS = 2
    
    def send_exception(self, module, service, function, ex_msg):
        message = ex_msg + "\n\n" + module + "\n" +  service + "\n" + function 
        print message  
        

    def savequeue(self , frm,to, date_time , email_cc, email_bcc , emailtype , subject , param ,dealer_id , attachment=None):
        '''region , timezone , ccs '''
        eq2 = EmailQueue(mail_to=to,mail_from=frm,type=emailtype , created_time = timezone.now() , subject = subject , cc =email_cc , bcc = email_bcc , mail_time = date_time, params=param, dealer_id = dealer_id )
        eq2.save()
        self.send_emails(eq2 , attachment)
        
        return eq2
    
    
    def send_emails(self,emailobj , attachment):
        #emailslist = EmailQueue.objects.filter(mail_time__lte=mail_time,status=self.PENDING_STATUS)
        #if emailslist.exists():
        if emailobj:
        #for  emailobj in emailslist:
            try:
                self.send_email(emailobj,attachment)
                emailobj.sent_time = timezone.now()
                emailobj.status =self.SENT_STATUS
                emailobj.mail_error = 0
            except Exception,e:
                print e
                emailobj.mail_error = 1
                emailobj.mail_retries = emailobj.mail_retries + 1
                emailobj.mail_detail = str(e)
                emailobj.mail_failuire_date = timezone.now()
            emailobj.save()
        else: 
            print "no email in queue"
#         self.update_emails_batch(mail_time,status=self.PENDING_STATUS,self.IN_QUEUE_STATUS)
    
    def send_email(self,emailobj,attachment):
        if emailobj:
            email_multimedia  = EmailMultimedia.objects.filter(dealer = emailobj.dealer)
            email_body,emailbodyhtml =self.get_email_body(emailobj)
            bcc = self.get_bcc(emailobj)
            cc = self.get_cc(emailobj)
            mail_to = self.get_to(emailobj)
            msg = EmailMultiAlternatives(emailobj.subject, emailbodyhtml, emailobj.mail_from, mail_to,bcc=bcc,cc=cc)
            msg.content_subtype = "html"
            for obj in email_multimedia:
                fp = open(os.path.join(settings.MEDIA_ROOT,'email_media/'+obj.multimedia_file), 'rb')
                msg_img = MIMEImage(fp.read())
                fp.close()
                msg_img.add_header('Content-ID', '<{}>'.format(obj.multimedia_file))
                msg.attach(msg_img)
            if attachment:
                msg.attach("CheckinReview.pdf", attachment, "application/pdf")              
            msg.send()
            print "mail sent"
    
    def get_email_body(self,emailobj):
        try:
            
            template_file_text = 'text/'+emailobj.type.template
            template_file_html = 'email/'+emailobj.type.html_template
            params = None
            try:
                params = json.loads(emailobj.params)
            except Exception:   
                print "unable to load"             
                pass 
            msg_plain = render_to_string(template_file_text,params)
            msg_html = render_to_string(template_file_html, params)            
            return (msg_plain,msg_html)
        except TemplateDoesNotExist:
            print "Template doesnot exist"
            raise TemplateDoesNotExist
        
        
    def get_to(self,emailobj):
        to = []
    
        try:                 
            to = emailobj.mail_to.split(",")
#             to = json.loads(emailobj.mail_to)
        except Exception,e:
            print "to not correct"
            print to
            raise Exception
        return to
    def get_bcc(self,emailobj):
        bcc = []
        try:            
            bcc = emailobj.bcc.split(",")
        except Exception,e:
            print "BCC not correct"
        return bcc
    
    def get_cc(self,emailobj):
        cc = []
        try:            
            cc = emailobj.cc.split(",")
        except Exception,e:
            print "CC not correct"
        return cc