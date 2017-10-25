import phonenumbers
from twilio.rest import TwilioRestClient

from BMW import settings


# Your Account Sid and Auth Token from twilio.com/user/account
class TwillioService():
    account_sid = "AC6168bee50e34f6fe6f1b021356bde3cc"
    auth_token  = "4754452df8b3386e34f60751f7682f9b"
    account_sid = settings.TWILIO_SID
    auth_token  = settings.TWILIO_AUT
    client = TwilioRestClient(account_sid, auth_token)
    default_number  = "+13312156289"
    default_number  = settings.TWILIO_DEFAULT
    def send_message(self,body,to,frm):
        try:
            if to.startswith("+")==False:
                to = "+"+to
            to = self.convert_to_e164(to)
            message = self.client.messages.create(body=body,
                                         to=to,
                                         from_=frm) # Replace with your Twilio number
            return message.id
        except Exception,e:
            print e
            
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