'''
Created on 17-Nov-2015

@author: Asim Riaz
'''


GROUP_NAME = "Dealer"

ADVISOR_GROUP_NAME = "Advisor"

REDIRECT_URL = "/dealership/login"
SENDER_EMAIL = "shoaibanwar1@gmail.com"
ADMIN_EMAIL = "ahmed.roofi@gmail.com"
SMTP_ADDRESS = "localhost"
PROTOCOL = "http://"

#Success Messages
#Login
REQUEST_EMAIL_SENT_MESSAGE = 'Email has been sent'
FIRSTLOGIN_MESSAGE = 'Password has been updated. Please provide the new credentials'
PASSCHANGE_MESSAGE = 'Password has been updated. Please provide the new credentials'
PASSCREATE_MESSAGE = 'Password has been updated. Please provide the new credentials'
RESET_EMAIL_SENT_MESSAGE = 'Email has been sent'

#Error Messages
#Login
LOGIN_USERNAME_DEALER_ERROR = "this user is not dealer"
LOGIN_USERNAME_ACTIVE_ERROR = "user is not active"
LOGIN_USERNAME_INCORRECT_ERROR = "username password incorrect"
LOGIN_USERNAME_ERROR = "Username not correct"

REQUEST_EMAIL_EXIST_ERROR = "account associated with this email already exists"
REQUEST_EMAIL_SENT_ERROR = "email sending failed"

PASSCHANGE_CURRENT_ERROR = "You have not provided the correct password"
PASSCREATE_ANSWER_ERROR = "You have not provided the correct answer"

RESET_EMAIL_SENT_ERROR = "email sending failed"
RESET_EMAIL_EXIST_ERROR = "email doesnot exist"
RESET_EMAIL_GROUP_ERROR = "email does not belong to the dealerhip"

DEALER_ID = 1
DEALER_SHOP_OPENING_HOUR = 07
DEALER_SHOP_OPENING_MINUTE = 00
DEALER_SHOP_CLOSING_HOUR = 17
DEALER_SHOP_OPENING_MINUTE = 00

