'''
Created on 17-Nov-2015

@author: Asim Riaz
'''

from functools import wraps
import test
import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs

from BMW import settings
from dealership.services.dealershipservice import DealerShipService

from . import conf


def dealer_group_check(user):
    if not user.groups.filter(name__in=[conf.GROUP_NAME]):
        return False
    return True

def dealer_allow_check(user):
    if not user.groups.filter(name__in=[conf.GROUP_NAME]):
        return False    
    if user.userprofile.terms_agreed == 'False':
        return False   
    request.session["group"] = conf.GROUP_NAME 
    return True

def advisor_allow_check(user):
    if not user.groups.filter(name__in=[conf.ADVISOR_GROUP_NAME]):
        return False
    if user.userprofile.terms_agreed == 'False':
        return False
    request.session["group"] = conf.GROUP_NAME
    return True

def dealership_access_check(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        group_name = ""
        if "dealer_code" not in request.session:
            return HttpResponseRedirect(reverse('dealership:login')) 
        else:
            dealer_code = request.session["dealer_code"]
            dealer_service = DealerShipService()
            dealership = dealer_service.get_dealer_by(dealer_code)
            request.session["dealer_code"] = dealer_code
            request.session["dealer_name"] = dealership.name
            request.session["dealer_id"] = dealership.id
            try:
                group_name = request.session["group"]
            except:
                for g in request.user.groups.all():
                    group_name = g.name
                    request.session["group"] = g.name
            if group_name in [conf.GROUP_NAME , conf.ADVISOR_GROUP_NAME] and request.user.userprofile.dealer.dealer_code == request.session["dealer_code"]:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('dealership:logout'))
                #return HttpResponseRedirect(reverse('dealership:login')+"?dealer_code="+request.session["dealer_code"])   
        
                 
    return wrap


def only_dealership_access_check(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        group_name = ""
        
        if "dealer_code" not in request.session:
            return HttpResponseRedirect(reverse('dealership:login')) 
        else:
            dealer_code = request.session["dealer_code"]
            dealer_service = DealerShipService()
            dealership = dealer_service.get_dealer_by(dealer_code)
            request.session["dealer_code"] = dealer_code
            request.session["dealer_name"] = dealership.name
            request.session["dealer_id"] = dealership.id
            try:
                group_name = request.session["group"]
            except:
                for g in request.user.groups.all():
                    group_name = g.name
                    request.session["group"] = g.name
            if group_name in [conf.GROUP_NAME,conf.ADVISOR_GROUP_NAME] and request.user.userprofile.dealer.dealer_code == request.session["dealer_code"]:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('dealership:logout'))
                #return HttpResponseRedirect(reverse('dealership:login')+"?dealer_code="+request.session["dealer_code"])   
        
                 
    return wrap

def dealership_services_access_check(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        for g in request.user.groups.all():
            group_name = g.name
        if group_name in [conf.GROUP_NAME, conf.ADVISOR_GROUP_NAME, "Customer"]:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('dealership:login')+"?dealer_code="+request.session["dealer_code"])   
    return wrap

def onlydealer_access_check(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if request.session["group"] == conf.GROUP_NAME:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('dealership:login')+"?dealer_code="+request.session["dealer_code"])   
    return wrap


def dealer_not_group_check(user):
    if not user.is_authenticated() and not user.groups.filter(name__in=[conf.GROUP_NAME]):
        return False
    return True



 


 

 
