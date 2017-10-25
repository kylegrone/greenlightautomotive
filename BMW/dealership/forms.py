import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from dealership.models import *
from dealership.widgets import QuestionChoiceField



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    
    
    
class LoginForm(forms.Form): 
    username_attrs = {"required": True,
                      "placeholder":"Username",
                      "class":"form-control"
                      }
    password_attrs = {"required": True,
                      "placeholder":"Password",
                      "class":"form-control",
                    "max_length":30, "render_value":False
                      }
#     dict(=True, max_length=30,placeholder="abc","class"="")
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=username_attrs), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    password = forms.CharField(widget=forms.PasswordInput(attrs= password_attrs), label=_("Password"))
    remember = forms.BooleanField(required=False,initial=False,label='Extra cheeze')
    
    
    
class ChangePasswordForm(forms.Form): 
    current_attrs = {"required": True,
                      "placeholder":"Enter Current Password",
                      "class":"form-control", "id":"current",
                      "max_length":30, "render_value":False
                      }
    new_attrs = {"required": True,
                      "placeholder":"Enter New Password",
                      "class":"form-control","id":"new",
                    "max_length":30, "render_value":False
                      }    
    confirm_attrs = {"required": True,
                      "placeholder":"Confirm Password",
                      "class":"form-control","id":"confirm",
                    "max_length":30, "render_value":False
                      }
    current = forms.CharField(widget=forms.PasswordInput(attrs= current_attrs), label=_("Current"))
    new = forms.CharField(widget=forms.PasswordInput(attrs= new_attrs), label=_("New"))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs= confirm_attrs), label=_("Confirm"))
    
    
    
class SecretQuestionForm(forms.Form): 
    new_attrs = {"required": True,
                      "placeholder":"Enter New Password",
                      "class":"form-control","id":"new",
                    "max_length":30, "render_value":False
                      }    
    confirm_attrs = {"required": True,
                      "placeholder":"Confirm Password",
                      "class":"form-control","id":"confirm",
                    "max_length":30, "render_value":False
                      }
    answer_attrs = {"required": True,
                      "placeholder":"Answer",
                      "class":"form-control","id":"answer",
                    "max_length":255, "render_value":False
                      }
    question_attrs = {"required": True,
                      "placeholder":"Question",
                      "class":"form-control","id":"question",
                    "render_value":False
                      }
    new = forms.CharField(widget=forms.PasswordInput(attrs= new_attrs), label=_("New"))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs= confirm_attrs), label=_("Confirm")) 
    questions = QuestionChoiceField(queryset=Questions.objects.all().order_by('id'),empty_label="Select a Question",widget=forms.Select(attrs=answer_attrs))
    answer = forms.CharField(widget=forms.TextInput(attrs=answer_attrs), label=_("Answer"))
    
    
class CreateUserForm(forms.Form): 
    user_attrs = {"required": True,
                      "placeholder":"Enter your username",
                      "class":"form-control","id":"user_name_id","data-error":"false",
                    "max_length":30, "render_value":False
                      }  
    profile_attrs = {"required": False,
                      "class":"form-control","id":"profile_user_id",
                    "max_length":30, "render_value":False
                      }      
    new_attrs = {"required": True,
                      "placeholder":"Enter New Password",
                      "class":"form-control","id":"new",
                    "max_length":30, "render_value":False
                      }    
    confirm_attrs = {"required": True,
                      "placeholder":"Confirm Password",
                      "class":"form-control","id":"confirm",
                    "max_length":30, "render_value":False
                      }

    username = forms.CharField(widget=forms.TextInput(attrs= user_attrs), label=_("User"))
    new = forms.CharField(widget=forms.PasswordInput(attrs= new_attrs), label=_("New"))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs= confirm_attrs), label=_("Confirm"))
    profile = forms.CharField(widget=forms.HiddenInput(attrs= profile_attrs))
    
class CreatePasswordForm(forms.Form): 
    new_attrs = {"required": True,
                      "placeholder":"Enter New Password",
                      "class":"form-control","id":"new",
                    "max_length":30, "render_value":False
                      }    
    confirm_attrs = {"required": True,
                      "placeholder":"Confirm Password",
                      "class":"form-control","id":"confirm",
                    "max_length":30, "render_value":False
                      }
    answer_attrs = {"required": True,
                      "placeholder":"Answer",
                      "class":"form-control","id":"answer",
                    "max_length":255, "render_value":False
                      }
    new = forms.CharField(widget=forms.PasswordInput(attrs= new_attrs), label=_("New"))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs= confirm_attrs), label=_("Confirm"))
    answer = forms.CharField(widget=forms.TextInput(attrs=answer_attrs), label=_("Answer"))
    
class UserPasswordResetForm(forms.Form): 
    new_attrs = {"required": True,
                      "placeholder":"Enter New Password",
                      "class":"form-control","id":"new",
                    "max_length":30, "render_value":False
                      }    
    confirm_attrs = {"required": True,
                      "placeholder":"Confirm Password",
                      "class":"form-control","id":"confirm",
                    "max_length":30, "render_value":False
                      }
#     answer_attrs = {"required": True,
#                       "placeholder":"Answer",
#                       "class":"form-control","id":"answer",
#                     "max_length":255, "render_value":False
#                       }
    new = forms.CharField(widget=forms.PasswordInput(attrs= new_attrs), label=_("New"))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs= confirm_attrs), label=_("Confirm"))
#     answer = forms.CharField(widget=forms.TextInput(attrs=answer_attrs), label=_("Answer"))
    

class ResetForm(forms.Form): 
    email_attrs = {"required": True,
                      "placeholder":"Email Address",
                      "class":"form-control","id":"email"
                      }       
    
    email = forms.EmailField(widget=forms.TextInput(attrs=email_attrs), label=_("Email address"))
    #question_list = Questions.objects.values_list('id', 'question_text')
    #questions = forms.ChoiceField(choices=[(x, y) for x,y in question_list])
    
class SearchCustomerForm(forms.Form):
    CHOICES=[('name', 'Name'),
             ('phone', 'Phone #'),
             ('email', 'Email'),
             ('vin', 'VIN #'),
             ('appt', 'Appt. Confirmation #')]
    
    criteria_attrs = {"required": True,
                      "placeholder":"Enter Search Criteria",
                      "class":"form-control","id":"criteria"
                      } 

    search_attrs = {"required": True
                      } 
    
    search = forms.ChoiceField(choices=CHOICES, initial='name', widget=forms.RadioSelect(attrs=search_attrs))
    criteria = forms.CharField(widget=forms.TextInput(attrs=criteria_attrs), label=_("Criteria"))
    
"""    
class AddServiceRepairForm(forms.Form):
    CHOICES=[('r', 'Repair'),
             ('s', 'Service')]
    
    type_attrs = {"required": True,
                      "class":"form-control form-service-type"
                      }
    
    id_attrs = {"required": False,
                      "class":"form-control form-service-id"
                      }
    
    name_attrs = {"required": True,
                      "class":"form-control form-service-name", "placeholder":"Enter Service Name"
                      } 
    
    code_attrs = {"required": True,
                      "class":"form-control form-service-code", "placeholder":"Enter DMS OpCode"
                      }
    
    duration_attrs = {"required": True,
                      "class":"form-control form-service-duration", "placeholder":"Enter Duration of Service"
                      }
    
    price_attrs = {"required": True,
                      "class":"form-control form-service-price", "placeholder":"Enter Price of Service"
                      }
   
    flag_attrs = {"required": False,
                      "class":"form-control form-service-flag",
                      "value":0
                      } 
    desc_attrs = {"required": True,
                      "class":"form-control form-service-desc", "rows":4,
                      "placeholder":"This is the description that will display for the customer. Edit description here"
                      }
    
    id = forms.CharField(widget=forms.HiddenInput(attrs=id_attrs)) 
    type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs=type_attrs))
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label=_("Name"))
    dms_opcode = forms.CharField(widget=forms.TextInput(attrs=code_attrs), label=_("DMS OpCode"))
    duration = forms.CharField(widget=forms.TextInput(attrs=duration_attrs), label=_("Duration"))
    price = forms.CharField(widget=forms.TextInput(attrs=price_attrs), label=_("Price"))
    flag_service = forms.CharField(widget=forms.HiddenInput(attrs=flag_attrs)) 
    description = forms.CharField(widget=forms.Textarea(attrs=desc_attrs), label=_("Description"))
"""    


class ManageServiceRepairForm(forms.ModelForm):
    
    class Meta:
        model = ServiceRepair
    
        type_attrs = {"required": True,
                          "class":"form-control form-service-type"
                          }
        
        dealer_id_attrs = {
                          "class":"form-control form-dealer-id"
                          }
        
        name_attrs = {"required": True,
                          "class":"form-control form-service-name", "placeholder":"Enter Service Name"
                          } 
        
        code_attrs = {"required": True,
                          "class":"form-control form-service-code", "placeholder":"Enter DMS OpCode"
                          }
        
        duration_attrs = {"required": True,
                          "class":"form-control form-service-duration", "placeholder":"Enter Duration of Service"
                          }
        
        price_attrs = {"required": True,
                          "class":"form-control form-service-price", "placeholder":"Enter Price of Service"
                          }
        price_unit = {"required": True,
                          "class":"form-control form-service-price-unit", "placeholder":"Enter Price Unit"
                          }
       
        flag_attrs = {
                          "class":"form-control form-service-flag",
                          "value":"False"
                          } 
        desc_attrs = {"required": True,
                          "class":"form-control form-service-desc", "rows":4,
                          "placeholder":"This is the description that will display for the customer. Edit description here"
                          }        
        
        fields = ["type","name","dms_opcode", "duration", "price","price_unit", "flag_service", "description", "dealer", "image"]
 
        widgets={ 
                "type" : forms.RadioSelect(attrs=type_attrs, choices = [('r', 'Repair'), ('s', 'Service')]),
                "name" : forms.TextInput(attrs=name_attrs),
                "dms_opcode" : forms.TextInput(attrs=code_attrs),
                "duration" : forms.TextInput(attrs=duration_attrs),
                "price" : forms.TextInput(attrs=price_attrs),
                "print_unit":forms.TextInput(attrs=price_unit),
                "flag_service" : forms.HiddenInput(attrs=flag_attrs), 
                "description" : forms.Textarea(attrs=desc_attrs),                
                "dealer" : forms.HiddenInput(attrs=dealer_id_attrs),
            }     
        image= forms.ImageField()
        
        
        
class GuestAppointmentForm(forms.ModelForm):
    
    class Meta:
        model = Appointment
        customer_attrs = {
                      "id":"customer_id_appt","class":"customer_id_hidden"
                      
                      }
        vehicle_attrs = {
                            "id":"vehicle_id_appt"
                            }
        
        advisor_attrs = {
                            "id":"advisor_id_appt"
                            }
        
        maintenance_attrs = {"required": True,
                    "class":"form-control maintenance_field"                      
                    }
        
        notes_attrs = {"required": False,
                    "class":"form-control notes_field",
                    "rows":2,
                    "placeholder":"Add Service Needs/Concerns here","render_value":False             
                    }
        
        fields = ["customer","vehicle","advisor", "maintenance", "service_notes"]
        
 
        widgets={
                  "customer":forms.HiddenInput(attrs=customer_attrs),
                  "vehicle":forms.HiddenInput(attrs=vehicle_attrs),
                  "advisor":forms.HiddenInput(attrs=advisor_attrs),
                  "maintenance":forms.RadioSelect(attrs=maintenance_attrs, choices = [(True,'Yes'),(False,'No')]),
                  "service_notes" : forms.Textarea(attrs=notes_attrs)
                } 

class GuestAccountForm(forms.Form): 
        CHOICES=[('phone', 'Phone'),
            ('email', 'Email'),
            ('text', 'Text')]

        method_of_reminder_attr= {"required": True,
                      "class":"form-control method_of_reminder_field"                      
                      }    
        
        customer_attrs = {'class':"customer_id_hidden"
                      }        
        method_of_reminder = forms.ChoiceField(choices=CHOICES, initial='email', widget=forms.RadioSelect(attrs=method_of_reminder_attr))
        customer = forms.CharField(widget=forms.HiddenInput(attrs=customer_attrs)) 
        
class CustomerInsuranceForm(forms.ModelForm):
    class Meta:
        model = DriverLiscenseIsurance
        YEARS =((n, n) for n in range(2015, 2030)) 
        MONTH_CHOICE = ((n, n) for n in range(1, 13))
        exclude = ['date_added','state','driver_liscens_number']
        insurancecompanyattrs = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter Insurance Company"
                 }
        insurancecardattrs = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter Insurance Card Number"
                 }
        
        exp_month_attr = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter Expiry Month"
                 }
        exp_year_attr = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter Expiry Year"
                 }
        
        widgets={
                      "insurance_company_name":forms.TextInput(attrs=insurancecompanyattrs),
                      "insurance_card_number":forms.TextInput(attrs=insurancecardattrs),
                      "ins_exp_year":forms.Select(attrs=exp_year_attr),
                      "ins_exp_month":forms.Select(attrs=exp_month_attr),
                      "user":forms.HiddenInput()
                  }
# class GuestccountForm(forms.Form):    
#         
#         CHOICES=[('phone', 'Phone'),
#              ('email', 'Email'),
#              ('text', 'Text')]
#         
#         MAINTENANCE=[('1', 'Yes'),
#              ('0', 'No')]
#         
#         first_name_attrs = {"required": True,
#                       "placeholder":"Enter First Name",
#                       "class":"form-control","id":"first_name_id",
#                     "max_length":30, "render_value":False
#                       }    
#         last_name_attrs = {"required": True,
#                       "placeholder":"Enter Last Name",
#                       "class":"form-control","id":"last_name_id",
#                     "max_length":30, "render_value":False
#                       } 
#         email_attr = {"required": True,
#                       "placeholder":"Enter email",
#                       "class":"form-control email_field",
#                      "max_length":255, "render_value":False
#                       }
#       
#         phone_attr = {"required": True,
#                       "placeholder":"Enter Phone",
#                       "class":"form-control phone_number_field",
#                     "max_length":255, "render_value":False
#                       }             
#         
#         register_link_attr= {"class":"form-control register_link_field"                         
#                        }
#         
#         reminder_attr= {"class":"form-control reminder_field",                           
#                        }
#         method_of_reminder_attr= {"required": True,
#                       "class":"form-control method_of_reminder_field"                      
#                       }
#         
#         vehicle_id_attr = {"required": True,
#                            "id":"vehicle_id_field"
#                            }
#         
#         mileage_attrs = {"required": False,
#                       "placeholder":"Enter Mileage",
#                       "class":"form-control","id":"mileage_vehicle",
#                       "max_length":30, "render_value":False
#                       }  
#           
#         liscense_attrs = {"required": False,
#                           "placeholder":"Enter Liscense",
#                           "class":"form-control","id":"liscense_vehicle",
#                         "max_length":30, "render_value":False
#                           }
#         
#         vin_number_attrs = {"required": False,
#                           "placeholder":"Enter Vin #",
#                           "class":"form-control","id":"vin_vehicle",
#                           "max_length":255, "render_value":False
#                           }
#         
#         maintenance_attrs = {"required": True,
#                       "class":"form-control maintenance_field"                      
#                       }
#         
#         notes_attrs = {"required": False,
#                       "class":"form-control notes_field",
#                       "rows":2,
#                       "placeholder":"Add Service Needs/Concerns here"                 
#                       }
#         
#        
#         first_name= forms.CharField(widget=forms.TextInput(attrs=first_name_attrs))
#         last_name = forms.CharField(widget=forms.TextInput(attrs=last_name_attrs))
#         phone_number_1 = forms.CharField(widget=forms.TextInput(attrs=phone_attr))
#         email_1 = forms.CharField(widget=forms.TextInput(attrs=email_attr))
#         register_link = forms.BooleanField()
#         reminder = forms.BooleanField()        
#         method_of_reminder = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs=method_of_reminder_attr))
#         vehicle_id = forms.CharField(widget=forms.HiddenInput(attrs=vehicle_id_attr)) 
#         
#         milage = forms.CharField(widget=forms.TextInput(attrs=mileage_attrs))
#         vin_number = forms.CharField(widget=forms.TextInput(attrs=vin_number_attrs))
#         
#         lisence_number = forms.CharField(widget=forms.TextInput(attrs=liscense_attrs))
#         
#         regular_maintenance = forms.ChoiceField(choices=MAINTENANCE, widget=forms.RadioSelect(attrs=maintenance_attrs))
#         notes = forms.CharField(widget=forms.Textarea(attrs=notes_attrs))
        
    
    
     