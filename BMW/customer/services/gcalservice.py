from __future__ import print_function

import datetime
import os
import os

from apiclient import discovery
from django.contrib import messages
from django.utils.timezone import get_current_timezone
import httplib2
from oauth2client import client
from oauth2client import client
from oauth2client import tools
import oauth2client


from BMW import settings
from customer.services.userservices import CUserService
from dealership.services.userservices import UserService
from dealership.views.appointment import appointment

class GCalService():
    client_id = "1067113358326-n89c21snjtu43v7711qjjvq2bjm5vop2.apps.googleusercontent.com"
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'BMW'
#     
#     def create_event(self,appointment,dealer):
#         try:
#             print "Her"
# #             event = {'summary':'Appointment',
# #                      'location':dealer.address_line1,
# #                      'description':"Appointment",
# #                      'start':{
# #                               "dateTime":appointment.start_time.isoformat(),
# #                               "timeZone":get_current_timezone()
# #                             },
# #                      'end':{
# #                               "dateTime":(appointment.start_time+ datetime.timedelta(minutes=20)).isoformat(),
# #                               "timeZone":get_current_timezone()
# #                             },
# #                      "atendess":[{"email":appointment.customer.email_1}],
# #                      "reminders":{"useDefault":True}}
#                      
#            
#             print "asda"
#         except Exception,e:
#             return False
        
         
    def get_credentials(self,appointment_id):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
        credential_dir = settings.MEDIA_ROOT #os.path.join(home_dir, '.credentials')
#         if not os.path.exists(credential_dir):
#             os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                        str(appointment_id)+'-gcal-credentials.json')
#     
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
#         credentials = None
        if not credentials :
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
#             else: # Needed only for compatibility with Python 2.6
#                 credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
    
#     def create_event(self,appointment,dealer):
#         try:
#             print appointment.start_time.isoformat()
#         except Exception,e:
# #             print e
#             return False