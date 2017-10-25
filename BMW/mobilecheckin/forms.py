from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User , Group
from dealership.models import *

from django.utils.safestring import mark_safe


class WalkinForm(forms.Form):
    
    name_attrs = {"required": True,
                      "placeholder":"Name",
                      "class":"form-control",
                      "name":"namee","render_value":False
                      
                      }
    phone_attrs = {"required": True,
                      "placeholder":"Phone",
                      "class":"form-control",
                      "name":"phone","render_value":False
                      
                      }
    email_attrs = {"required": True,
                      "placeholder":"Email",
                      "class":"form-control",
                      "name":"email","render_value":False
                      
                      }
    
   
    year_attrs = {"required": True,
                      "placeholder":"role",
                      "class":"form-control",
                      "name":"year","render_value":False
                      } 
    model_attrs = {"required": True,
                      "placeholder":"role",
                      "class":"form-control",
                      "name":"model","render_value":False
                      } 
    make_attrs = {"required": True,
                      "placeholder":"role",
                      "class":"form-control",
                      "name":"make","render_value":False
                } 
    
    vin_attrs = {"required": False,
                      "placeholder":"team",
                      "class":"form-control",
                      "name":"team","render_value":False
                }
   
    vid_attrs = {"required": False,
                      "placeholder":"vehicle id",
                      "class":"form-control",
                      "name":"vehicle_id","render_value":False,"id":"vehicle_id_field"
                }
    
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs))
    phone = forms.CharField(widget=forms.TextInput(attrs=phone_attrs) )
    email = forms.CharField(widget=forms.TextInput(attrs=email_attrs))
#     year = forms.ChoiceField(widget = forms.Select(attrs = year_attrs) , choices = ([(x.id, x.name) for x in VinYear.objects.all()]))
#     make = forms.ChoiceField(widget = forms.Select(attrs = make_attrs) , choices = ([(x.id, x.name) for x in VinMake.objects.all()]))
#     model = forms.ChoiceField(widget = forms.Select(attrs = model_attrs) , choices = ([(x.id, x.name) for x in VinModel.objects.all()]))
    vin = forms.CharField(widget=forms.TextInput(attrs=vin_attrs))
    vehicle_id = forms.CharField(widget=forms.HiddenInput(attrs=vid_attrs))
    