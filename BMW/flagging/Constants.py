'''
Created on Nov 18, 2015

@author: mjnasir
'''
from django.core.urlresolvers import reverse


TECHNICIAN = "Technician"
ADVISOR = "Advisor"
DEALER = "Dealer"
REDIRECT_URL = "flagging:login"
fields_dictionary = {"RO Number" : "ro_number",
                     "RO Date" : "ro_date",
                     "TAG/RFID": "rfid_tag",
                     "CUSTOMER":"customer",
                     "YEAR":"year",
                     "MAKE":"make",
                     "MODEL":"model",
                     "ODOMETER":"odometer",
                     "ADVISOR":"advisor",
                     "INSPECTOR":"inspector"
                     }
