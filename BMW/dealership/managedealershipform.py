'''
Created on Jan 4, 2016

@author: aroofi
'''
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User , Group
from dealership.models import *

from django.utils.safestring import mark_safe

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
    
class DetailForm(forms.ModelForm):
    class Meta:
        model = Dealer
        name_attrs = {"required": True,
                          "placeholder":"Enter Shop Name",
                          "class":"form-control",
                          
                          }
        dealercode_attrs = {"required": True,
                          "placeholder":"Enter Dealer Code",
                          "class":"form-control",
                          
                          }
        description_attrs = {"required": False,
                          "placeholder":"Enter Description",
                          "class":"form-control",
                          "rows":0,
                          "cols":0,
                          }
        address_attrs = {"required": False,
                          "placeholder":"Enter Address",
                          "class":"form-control",
                          "rows":0,
                          "cols":0,
                          }
        timezone_attrs = {"required": False,
                          "placeholder":"Timezone",
                          "class":"form-control",
        
                          }
        consumeraccess_attrs = {"required": False,
                          "class":""
                          }
        webkey_attrs = {"required": False,
                          "placeholder":"Enter WebKey",
                          "class":"form-control",
                          }
        frameset_attrs = {"required": False,
                          "placeholder":"Enter FrameSet URL",
                          "class":"form-control",
                          }
        service_attrs = {"required": False,
                          "placeholder":"Enter Service URL",
                          "class":"form-control",
                          }
        DMS_attrs = {"required": False,
                          "class":""
                          }
        customer_attrs = {"required": False,
                          "placeholder":"customer",
                          "class":"form-control",
                          }
        msg_attrs = {"required": False,
                        "placeholder":"Message of the Day",
                        "class":"form-control",
                        "cols":0,
                        "rows":4,
                    }
        privacy_attrs = {"required": False,
                          "placeholder":"Copy & Past Private Policy",
                          "class":"form-control",
                          "cols":0,
                          "rows":4,
                          }
        fields = ('name','dealer_code' ,'address_line1', 'description' ,'timezone' ,'privacy_polilcy' , 'privacy_policy' , 'message_of_the_day','webkey',
                  'frameset_url','service_url','dms_access','consumer_access')
                   
        widgets = {
                    'name' : forms.TextInput(attrs=name_attrs),
                    'dealer_code' : forms.TextInput(attrs=dealercode_attrs),
                    'address_line1' : forms.Textarea(attrs = address_attrs ),
                    'description' : forms.Textarea(attrs = description_attrs ),
                    'timezone' : forms.Select(attrs = timezone_attrs,choices = [(x.timezone, x.name) for x in TimeZones.objects.all()]) ,
                    'consumer_access':  forms.RadioSelect(attrs = consumeraccess_attrs,renderer=HorizontalRadioRenderer,choices = ((True,'Yes'),(False,'No'))),
                    'webkey' : forms.TextInput(attrs=webkey_attrs) ,
                    'frameset_url' : forms.TextInput(attrs=frameset_attrs) ,
                    'service_url' : forms.TextInput(attrs=service_attrs) ,
                    'dms_access' : forms.RadioSelect(attrs = DMS_attrs,renderer=HorizontalRadioRenderer,choices = ((True,'Activate'),(False,'Deactivate'))), 
                    'customer' : forms.Select(attrs = customer_attrs ) , 
                    'message_of_the_day' : forms.Textarea(attrs = msg_attrs ),
                    'privacy_policy' : forms.Textarea(attrs = privacy_attrs ),
        
                }
        
class NewUserAdvisorForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(NewUserAdvisorForm, self).__init__(*args, **kwargs)
        team_attrs = {"required": False,
                      "placeholder":"team",
                      "class":"form-control",
                      "name":"team","render_value":False
                      }
        self.fields['team'] = forms.ChoiceField(widget = forms.SelectMultiple(attrs = team_attrs) , choices = ([(x.id, x.name) for x in Team.objects.filter(created_by_id=user)]))
    
    username_attrs = {"required": True,
                      "placeholder":"Username",
                      "class":"form-control",
                      "name":"username","render_value":False
                      
                      }
    password_attrs = {"required": True,
                      "placeholder":"Create Temporary Password",
                      "class":"form-control",
                      "name":"password",
                    "max_length":30, "render_value":False
                      }
    first_attrs = {"required": True,
                      "placeholder":"Enter First Name",
                      "class":"form-control",
                      "name":"first","render_value":False
                      }
    last_attrs = {"required": True,
                      "placeholder":"Enter Last Name",
                      "class":"form-control",
                      "name":"last","render_value":False
                      }
    email_attrs = {"required": True,
                      "placeholder":"Enter Email",
                      "class":"form-control",
                      "name":"email","render_value":False,"type":"email"
                      }
    phone1_attrs = {"required": True,
                      "placeholder":"Enter Phone 1",
                      "class":"form-control",
                      "name":"phone1","render_value":False
                      }
    phone2_attrs = {"required": False,
                      "placeholder":"Enter Phone 2",
                      "class":"form-control",
                      "name":"phone2","render_value":False
                      }
    employee_attrs = {"required": True,
                      "placeholder":"Enter Employee Number",
                      "class":"form-control",
                      "name":"employee","render_value":False,
                      }
    role_attrs = {"required": True,
                      "placeholder":"role",
                      "class":"form-control",
                      "name":"role","render_value":False
                      } 
    team_attrs = {"required": False,
                      "placeholder":"team",
                      "class":"form-control",
                      "name":"team","render_value":False
                      }
    reserve_attrs = {"required": False,
                      "placeholder":"reserve",
                      "class":"form-control",
                      "name":"reserve","render_value":False
                      }
    user_id = forms.CharField(widget=forms.HiddenInput())
    first = forms.CharField(widget=forms.TextInput(attrs=first_attrs))
    last = forms.CharField(widget=forms.TextInput(attrs=last_attrs) )
    email = forms.CharField(widget=forms.TextInput(attrs=email_attrs))
    phone1 = forms.CharField(widget=forms.TextInput(attrs=phone1_attrs))
    phone2 = forms.CharField(widget=forms.TextInput(attrs=phone2_attrs))
    employee = forms.CharField(widget=forms.TextInput(attrs=employee_attrs))
    role = forms.ChoiceField(widget = forms.Select(attrs = role_attrs) , choices = ([(x.id, x.name) for x in Group.objects.exclude(name= 'Customer')]))
    #team = forms.ChoiceField(widget = forms.SelectMultiple(attrs = team_attrs) , choices = ([(x.id, x.name) for x in Team.objects.all()]))
    reserve = forms.ChoiceField(widget = forms.RadioSelect(attrs = reserve_attrs,renderer=HorizontalRadioRenderer), choices = ((1,'Yes'),(0,'No')), initial=1)
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=username_attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs= password_attrs))
    
    
class PackageForm(forms.Form):
    title_attrs = {"required": True,
                   "placeholder":"New Package Title",
                   "class":"form-control",
                   "render_value":False,
                   "name":"PackTitle"
                  }
    
    pack_name = forms.CharField(widget=forms.TextInput(attrs=title_attrs) ,label=_("New Package Title"))

class ItemForm(forms.Form):
    title_attrs = {"required": True,
                   "placeholder":"New Item Title",
                   "class":"form-control",
                   "render_value":False,
                   "name":"PackTitle"
                  }
    
    item_name = forms.CharField(widget=forms.TextInput(attrs=title_attrs) ,label=_("New Item Title"))
    
class NewFlagForm(forms.Form):
    title_attrs = {"required": True,
                   "placeholder":"Flag Name",
                   "class":"form-control",
                   "render_value":False,
                   "name":"aflagname"
                  }
    
    flag_name = forms.CharField(widget=forms.TextInput(attrs=title_attrs) ,label=_("Flag Name"))

class CategoryForm(forms.Form):
    cat_title = {"required": True,
                   "placeholder":"Category Title",
                   "class":"form-control",
                   "render_value":False,
                   "name":"Cattitle"
                 }
    cat_name = forms.CharField(widget=forms.TextInput(attrs=cat_title) ,label=_("New Package Title"))
    
    
    
class BmwResourceForm(forms.Form):
    name_attrs = {"required": False,
                      "placeholder":"Name Link",
                      "class":""
                      }
    rank_attrs = {"required": False,
                      "placeholder":"Order of Url",
                      "class":""
                      }
    url_attrs = {"required": False,
                      "placeholder":"Add Url",
                      "class":""
                      }
    
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs) ,label=_("Name of link"))
    url = forms.CharField(widget=forms.TextInput(attrs=url_attrs) ,label=_("URL"))
    rank = forms.ChoiceField(widget = forms.Select(attrs = rank_attrs) , choices = () ,label =_("Order of URL"))