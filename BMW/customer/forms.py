from django import  forms
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from django_countries.widgets import CountrySelectWidget

from dealership.models import *
from dealership.widgets import StateChoiceField, TrimChoiceField
from livechat.models import Upload

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    
    
class UploadVinForm(forms.ModelForm):
    class Meta:
        model = Upload
        pic_attr = {
                      'class':"upload_vin_button","id":"vin_upload"
                      
                      }
        widgets={
                  "pic":forms.FileInput(attrs=pic_attr),
                  
                } 
        fields = ["pic"]
        
        
class CreditDebitForm(forms.ModelForm):
    
    
    class Meta:
        model = CreditCardInfo
        YEARS =((n, n) for n in range(2015, 2030)) 
        MONTH_CHOICE = ((n, n) for n in range(1, 13))
        exclude= [ "date_added"]
        first_name_attr = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter First Name "
                 }
        last_name_attr = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter Last Name"
                 }
        
        card_type_attr = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Select Card type"
                 }
        card_number_attr = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter Card Number"
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
        car_ver_attr = {
                    "required":True,
                     "class":"form-control ",
                    "placeholder":"Enter Card Verification #"
                 }
        
        widgets={
                     "first_name":forms.TextInput(attrs=first_name_attr),
                     "last_name":forms.TextInput(attrs=last_name_attr),
                     "card_number":forms.TextInput(attrs=card_number_attr),
                     "card_type":forms.Select(attrs=card_type_attr),
                     "card_exp_year":forms.Select(attrs=exp_year_attr),
                     "card_exp_month":forms.Select(attrs=exp_month_attr),
                     "card_ver_number":forms.TextInput(attrs=car_ver_attr),
                      "user":forms.HiddenInput()
                  } 



class CustomerInsuranceForm(forms.ModelForm):
    state_attr = {"required": True,
                      "placeholder":"Enter State",
                      "class":"form-control",
                    "    max_length":30, "render_value":False
                      } 
    state_us = StateChoiceField(queryset=States.objects.all().order_by('id'),
                                                empty_label="Select a State",widget=forms.Select(attrs=state_attr))
    class Meta:
        model = DriverLiscenseIsurance
        exclude = ['date_added','state','ins_exp_year','ins_exp_month']
        driverliscattrs = {
                    "required":False,
                     "class":"form-control ",
                    "placeholder":"Enter Driver Liscense #"
                 }
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
        widgets={
                      "driver_liscens_number":forms.TextInput(attrs=driverliscattrs),
                      "insurance_company_name":forms.TextInput(attrs=insurancecompanyattrs),
                      "insurance_card_number":forms.TextInput(attrs=insurancecardattrs),
                      "user":forms.HiddenInput()
                  }
        
        
class GuestccountForm(forms.ModelForm):
    

    class Meta:
        model = UserProfile
        first_name_attrs = {"required": True,
                      "placeholder":"*Enter First Name",
                      "class":"form-control","id":"first_name_id",
                    "max_length":30, "render_value":False
                      }    
        last_name_attrs = {"required": True,
                      "placeholder":"*Enter Last Name",
                      "class":"form-control","id":"last_name_id",
                    "max_length":30, "render_value":False
                      } 
        email_attr = {"required": True,
                      "placeholder":"*Enter email",
                      "class":"form-control email_field",
                     "max_length":255, "render_value":False
                      }
      
        phone_attr = {"required": True,
                      "placeholder":"*Enter Phone",
                      "class":"form-control phone_number_field",
                    "max_length":255, "render_value":False
                      }
       
        method_of_contact_attr= {"required": False,
                      "placeholder":"Select Type",
                      "class":"form-control method_of_contact_field",
                      "max_length":255, "render_value":False
                      }
      
        
        fields = [
                 
                  "method_of_contact","email_1","phone_number_1",
                  "first_name","last_name"]
        
       
        widgets={   "first_name":forms.TextInput(attrs=first_name_attrs),
                    "last_name":forms.TextInput(attrs=last_name_attrs),
                    "phone_number_1":forms.TextInput(attrs=phone_attr),
                    "email_1":forms.TextInput(attrs=email_attr),
                    "method_of_contact":forms.Select(attrs=method_of_contact_attr)
                  } 
     
        
class CustomerAccountForm(forms.ModelForm):
    state_attr = {"required": True,
                      "placeholder":"Enter State",
                      "class":"form-control","id":"state_id",
                    "max_length":30, "render_value":False
                      }  
    
    phone_1_attrs = {"required": True,
                      "placeholder":"Enter Phone",
                      "class":"form-control phone_field",
                    "max_length":30, "render_value":False
                      }   
    
    email_1_attrs = {"required": True,
                      "placeholder":"Enter Email ",
                      "class":"form-control email_field",
                    "max_length":30, "render_value":False
                      }
    choice_attrs = {"required": True,
                      
                      "class":"form-control choice",
                   "render_value":False
                      }
    
#     first_name = forms.CharField(widget=forms.TextInput(attrs=first_name_attrs))
#     last_name = forms.CharField(widget=forms.TextInput(attrs=last_name_attrs))
    state_us = StateChoiceField(queryset=States.objects.all().order_by('id'),
                                                empty_label="Select a State",widget=forms.Select(attrs=state_attr))
    class Meta:
        model = UserProfile
        first_name_attrs = {"required": True,
                      "placeholder":"Enter First Name",
                      "class":"form-control","id":"first_name_id",
                    "max_length":30, "render_value":False
                      }    
        last_name_attrs = {"required": True,
                      "placeholder":"Enter Last Name",
                      "class":"form-control","id":"last_name_id",
                    "max_length":30, "render_value":False
                      } 
        email_attr = {"required": True,
                      "placeholder":"Enter email",
                      "class":"form-control email_field",
                     "max_length":255, "render_value":False
                      }
        email_opt_attr = {
                      "placeholder":"Enter email",
                      "class":"form-control email_field",
                     "max_length":255, "render_value":False
                      }
        
        phone_attr = {"required": True,
                      "placeholder":"Enter Phone",
                      "class":"form-control phone_number_field",
                    "max_length":255, "render_value":False
                      }
        phone_opt_attr = {
                      "placeholder":"Enter Phone",
                      "class":"form-control phone_number_field",
                    "max_length":255, "render_value":False
                      }
        phone_type_attr = {"required": True,
                      "placeholder":"Select Type",
                      "class":"form-control phone_number_type_field",
                    "max_length":255, "render_value":False
                      }
        country_attr = {"required": True,
                      "placeholder":"Select Country",
                      "class":"form-control country_field",
                    "max_length":255, "render_value":False
                      }
        method_of_contact_attr= {"required": True,
                      "placeholder":"Select Type",
                      "class":"form-control method_of_contact_field",
                    "max_length":255, "render_value":False
                      }
        
          
        city_attrs = {"required": True,
                      "placeholder":"Enter City",
                      "class":"form-control","id":"city_id",
                    "max_length":30, "render_value":False
                      }  
        zip_attrs = {"required": True,
                      "placeholder":"Enter Zip Code",
                      "class":"form-control","id":"zip_id",
                    "max_length":30, "render_value":False
                      }   
        address1_attrs = {"required": True,
                      "placeholder":"Enter Address",
                      "class":"form-control","id":"address_id",
                    "max_length":2000, "render_value":False
                      }
        address2_attrs = {
                      "placeholder":" ",
                      "class":"form-control","id":"address_2_id",
                      "max_length":2000, "render_value":False
                      }
        
        fields = ["city","zipcode","address_line1",
                  "address_line2","country","user",
                  "method_of_contact","email_1","email_2",
                  "phone_number_1","phone_1_type",
                  "phone_number_2","phone_2_type",
                  "phone_number_3","phone_3_type","method_of_contact",
                  "first_name","last_name"]
       
        widgets={   "first_name":forms.TextInput(attrs=first_name_attrs),
                    "last_name":forms.TextInput(attrs=last_name_attrs),
                    "zipcode":forms.TextInput(attrs=zip_attrs),
                    "city":forms.TextInput(attrs=city_attrs),
                    "address_line1":forms.TextInput(attrs=address1_attrs),
                    "address_line2":forms.TextInput(attrs=address2_attrs),
                    "country":CountrySelectWidget(attrs=country_attr),"user":forms.HiddenInput(),
                    "phone_number_1":forms.TextInput(attrs=phone_attr),
                    "phone_number_2":forms.TextInput(attrs=phone_opt_attr,)
                    ,"phone_number_3":forms.TextInput(attrs=phone_opt_attr),
                     "phone_1_type":forms.Select(attrs=phone_type_attr),
                     "phone_2_type":forms.Select(attrs=phone_type_attr),
                     "phone_3_type":forms.Select(attrs=phone_type_attr),
                     "email_1":forms.TextInput(attrs=email_attr),
                     "email_2":forms.TextInput(attrs=email_opt_attr),
                     "method_of_contact":forms.Select(attrs=method_of_contact_attr)
                  } 

class CustomerVehichleForm(forms.ModelForm):
    trim_attrs = {"required": False,
                      "placeholder":"Enter Trim",
                      "class":"form-control","id":"trim_vehicle",
                      "max_length":300, "render_value":False
                      } 
    trim = TrimChoiceField(queryset=VinTrim.objects.all().order_by('id'),
                                                empty_label="Select a Trim",widget=forms.Select(attrs=trim_attrs),required=False)
    class Meta:
        model = CustomerVehicle
        exclude = ['created_at','vin_image','vin_process',"trim","vin_data"]
        
        mileage_attrs = {"required": False,
                      "placeholder":"Enter Mileage",
                      "class":"form-control","id":"mileage_vehicle",
                    "max_length":30, "render_value":False
                      }    
        liscense_attrs = {"required": False,
                          "placeholder":"Enter License",
                          "class":"form-control","id":"liscense_vehicle",
                        "max_length":30, "render_value":False
                          }
        vin_number_attrs = {"required": False,
                          "placeholder":"Enter Vin #",
                          "class":"form-control","id":"vin_vehicle",
                        "max_length":255, "render_value":False
                          }
        vin_data_attrs = {"required": False,
                          "placeholder":"Enter Vin #",
                          "class":"form-control",
                          "id":"vin_data","style":"display:none",
                         "render_value":False
                          }
        color_attrs = {"required": False,
                          "placeholder":"Enter Color",
                          "class":"form-control","id":"color_vehicle",
                        "render_value":False
                          }
        
        customer_vehicle_desc_attr = {"required": False,
                          "placeholder":"Enter Desc",
                          "class":"form-control","id":"customer_vehicle_desc",
                        "render_value":False,
                         
                          }
        user_attrs = {
                      "id":"user_id_vehicle", "class":"customer_id_hidden"
                      
                      }
        vehicle_id_attrs = {
                            "id":"vehicle_id_field"
                            }
        widgets={
                      "lisence_number":forms.TextInput(attrs=liscense_attrs),
                      "milage":forms.TextInput(attrs=mileage_attrs),
                      "vin_number":forms.TextInput(attrs=vin_number_attrs),
                      "user":forms.HiddenInput(attrs=user_attrs),
                      "vehicle":forms.HiddenInput(attrs=vehicle_id_attrs),
                      "color":forms.TextInput(attrs=color_attrs),
#                     "vin_data":forms.Textarea(attrs=vin_data_attrs),
                    "customer_vehicle_desc":forms.Textarea(attrs=customer_vehicle_desc_attr),
#                      "trim":forms.Select(attrs=trim_attrs),
                  } 
        

        
        