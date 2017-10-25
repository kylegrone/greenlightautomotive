
import os

from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import pytesseract

from customer.app_confg import confg
from customer.decorators.decorators import customer_group_check
from customer.forms import CustomerVehichleForm, CustomerAccountForm, \
    CustomerInsuranceForm, CreditDebitForm

from dealership.forms import ChangePasswordForm

from customer.factories import CustomerServicesFactory
import json as mainjson
from livechat.forms import UploadForm


@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)
def delete(request):
        try:
            customer_factory = CustomerServicesFactory()
            user = request.user
            service = customer_factory.get_instance("account")#AccountService()
            resp = service.delete_account(user.userprofile)
            if resp:
                messages.success(request, "Account Deleted Successfully")
            else:
                messages.success(request, "Unable to Delete Account")
        except:
            messages.error(request, "Unable to  Deleted account. Try later")
        return HttpResponseRedirect(reverse("customer:accountsettings"))
    
    
@user_passes_test(customer_group_check,login_url=confg.REDIRECT_URL)     
def accountview(request):
    """
            This is the account view where oyu can sae the account information
    """
    customer_factory = CustomerServicesFactory()
    user = request.user
    dealer_code = request.session["dealer_code"]
    account_service =  customer_factory.get_instance("account")
    service = customer_factory.get_instance("user")
    template_name = 'customer/customer_account.html'
    name = request.user.first_name+" "+request.user.last_name
    userprofile =service.get_userprofile(request.user)
    insurance_profile = service.get_user_driver_insurance(userprofile)
    cc_profile = service.get_cc_profile(userprofile)
    account_initial = account_service.get_initial_user_form(user, userprofile)
    driver_initial  =account_service.get_initial_driver_form(user, insurance_profile,userprofile)
    cc_initial = account_service.get_initial_cc_form(user,cc_profile,userprofile)
    customer_form =CustomerAccountForm(instance=userprofile,initial=account_initial)
    driver_form = CustomerInsuranceForm(instance=insurance_profile,initial=driver_initial)
    cc_form = CreditDebitForm(instance=cc_profile,initial=cc_initial)
    pass_form = ChangePasswordForm() 
    tab = "account"
    
    if request.method == 'POST':
        resp = False
        password_changed=False
        
        if request.POST.get("type") == "account":
            
            customer_form = CustomerAccountForm(request.POST,instance=userprofile)
            resp = account_service.save_account_form(user,userprofile,customer_form,account_initial)
            msg = "Account Information saved  successfully" #
            
        elif request.POST.get("type")=="driver":
            driver_form = CustomerInsuranceForm(request.POST,instance = insurance_profile)
            resp = account_service.save_driver_form(insurance_profile,driver_form)
            msg = "Driver Liscense and Insurance Information saved  successfully"
            
        elif request.POST.get("type")=="cc":
            cc_form = CreditDebitForm(request.POST,instance = cc_profile)
            resp = account_service.save_cc_form(cc_profile,cc_form)
            msg =  "Debit/Credit form save successfully"
            
        elif request.POST.get("type")=="change_password":
            pass_form = ChangePasswordForm(request.POST)    
            resp = account_service.save_password_form(pass_form,user)    
            msg =  "Password Changed successfully"
            password_changed = True
        if password_changed:
            messages.success(request, msg)
            return  HttpResponseRedirect(reverse("customer:index")+"?dealer_code="+dealer_code)
        elif resp:
            messages.success(request, msg)
            return  HttpResponseRedirect(reverse("customer:accountsettings"))
        
            
    else:
        customer_form = CustomerAccountForm(instance=userprofile,initial=account_initial)
        driver_form = CustomerInsuranceForm(instance=insurance_profile,initial=driver_initial)
        cc_form = CreditDebitForm(instance=cc_profile,initial=cc_initial)
        pass_form = ChangePasswordForm() 
        
    
    context = {"page_title":"Customer Profile","tab":tab,
                                          "customer_form":customer_form,
                                          "driver_form":driver_form,
                                          "cc_form":cc_form,
                                          "pass_form":pass_form,
                                         "dealer_code":dealer_code,
                                          'acitve' : True,
                                          }
    service.set_centrifuge_context(request,dealer_code,userprofile, context,chatposition="top")
    return render(request, template_name,context)
    
    
    
    

#     return CustomerAccountForm(initial=initial,instance=userprofile) 
      
    
                  
    