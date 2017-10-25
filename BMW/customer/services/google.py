import argparse
import datetime
import os
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, request
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import get_current_timezone
from googleapiclient import discovery
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_orm import Storage

from BMW import settings
from apiclient.discovery import build
# from customer.models import CredentialsModel, FlowModel


class GoogleService():
    client_id = "1067113358326-esrmbu4e3np6mnohbv7phbopc2rsph7a.apps.googleusercontent.com"
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'client_secrets.json'
    
    APPLICATION_NAME = 'BMW'
    def create_event(self,appointment,credentials):
        try:
            http = httplib2.Http()
            http = credentials.authorize(http)
#             credentials  = self.get_credentials(appointment.id)
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)
            
            event = {'summary':'Appointment with '+appointment.dealer.name,
                    'location':appointment.dealer.address_line1,
                    'description':"You have an appointment with  "+appointment.dealer.name,
                    'start':{
                             "dateTime":appointment.start_time.isoformat(),
#                              "timeZone":get_current_timezone()
                           },
                    'end':{
                             "dateTime":(appointment.start_time+ datetime.timedelta(minutes=20)).isoformat(),
#                              "timeZone":get_current_timezone()
                           },
                    "atendess":[{"email":appointment.customer.email_1}],
                    "reminders":{"useDefault":True}}
            event = service.events().insert(calendarId='primary', body=event).execute()
#             print "Event created: %s' % (event.get('htmlLink'))
            
            return True
        except Exception,e:
            print e
            return False
            
            
    def get_credentials(self,appointment):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        pass
 