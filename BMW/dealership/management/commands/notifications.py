import json
import datetime
from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from dealership.models import * 
from dealership.factories import DealerShipServicesFactory
from dealership.services.emailservice import EmailService

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        dealer_factory = DealerShipServicesFactory()
        notificationservice = dealer_factory.get_instance("notification")
        appointmentservice  = dealer_factory.get_instance("appointment")
        appointments = appointmentservice.get_active_appointments_pending_reminder()
        #template = "email/appointment_reminder.html"
        #template_text = "text/appointment_reminder.html"
        if appointments:
            for obj in appointments:
                send_text=False
                if obj.customer:
                    app_service = AppointmentService.objects.filter(appointment_id = obj.id)
                    service_name = []
                    for obj in app_service:
                        service_name.append(obj.service.name)
                    notification_settings = notificationservice.get_schedlued_settings(obj.customer)
                    
                    if notification_settings:
                        if notification_settings["text"] == True:
                            send_text=True
                    context = {"name" : obj.customer.first_name+" "+obj.customer.last_name , "c_code": obj.confirmation_code , "start_time": obj.start_time.strftime('%B %d %Y %I:%M %p'),
                               "vehicle" : obj.vehicle.vehicle.make.name+" "+ obj.vehicle.vehicle.model.name , "advisor": obj.advisor.userprofile.first_name+" "+ obj.advisor.userprofile.last_name,
                               "g_cyl": settings.SITE_MAIN_URL+reverse('customer:sync_gcalendar')+"?appointment_id="+str(obj.id),
                               "o_cyl": settings.SITE_MAIN_URL+reverse('customer:download_calendar')+"?appointment_id="+str(obj.id),
                               "service_name": service_name,"wayaway":obj.way_away.name}
                    param = json.dumps(context)
                    emailtype = EmailTypes.objects.get(name="reminder")
                    email = EmailService()
                    frm = "bmw@dealership.com" 
                    subject = emailtype.subject
                    date_time = timezone.now()
                    status = email.savequeue( frm , obj.customer.email_1, date_time , "", "" , emailtype , subject , param,obj.dealer.id)
                    if send_text == True:
                        notificationservice.send_text_notification(obj.customer,email,context)

                        #status = notificationservice.send_notification(obj.customer,settings.EMAIL_HOST_USER,
                        #                                               template,template_text,
                        #                                      "BMW service Appointment Reminder",
                        #                                      {"main_url":settings.SITE_MAIN_URL,
                        #                                      "appointment":obj},send_text=send_text)
                    if status:
                        obj.appointment_reminder_status = True
                        obj.save()
        else:
            print "No APpointments"
                
            
        
        

        