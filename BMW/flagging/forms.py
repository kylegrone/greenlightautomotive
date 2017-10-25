'''
Created on Nov 20, 2015

@author: mjnasir

'''
from django import forms
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from dealership.models import UserProfile



class NewUserEmailForm(forms.Form):
    email_attrs = {"required": True,
                      "placeholder":"Email Address",
                      "class":"form-control","id":"email"
                      }       
    
    email = forms.EmailField(widget=forms.TextInput(attrs=email_attrs), label=("Email address"))

class TempNumberForm(forms.Form):
    number_attrs = {"required": True,
                    "placeholder" : "Phone Number",
                    "class": "form-control","id":"number"
                    }
    number = forms.IntegerField(widget=forms.TextInput(attrs=number_attrs),label=("Phone Number"))
    
class SkipConfirmationForm(forms.Form):
    skip = forms.BooleanField(required=False,initial=False,label='skip')
    
class UpdateNumberOrEmailForm(forms.Form):
    field_attrs = {"required": True,
                    "class": "form-control","id":"modeId",
                    "placeholder":"Phone Number"
                    }
    field = forms.CharField(widget=forms.TextInput(attrs=field_attrs), label=_("field"))