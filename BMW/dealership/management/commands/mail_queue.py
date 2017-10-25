'''
Created on May 68, 2015

@author: asima
'''
from datetime import datetime
from email.mime import application
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from dealership.services.emailservice import EmailService
from dealership.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        mail_time = timezone.now()
        email_service = EmailService()
        email_service.send_emails(mail_time)
                
    
        
    