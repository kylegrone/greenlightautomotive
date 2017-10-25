'''
Created on Dec 26, 2015

@author: mjnasir
'''
from datetime import datetime, timedelta
import datetime

from django import template
from django.shortcuts import render
from django.template import Context, Template
from django.utils import timezone
from django.utils.timezone import get_current_timezone
import pytz

import dealership
from dealership.factories import DealerShipServicesFactory
from dealership.models import RO, Notes, RoInspection, Dealer
from flagging.services.RoServices import RoServices


register = template.Library()


@register.simple_tag
def dealer_detail_tag(dealer_code):
    service_factory = DealerShipServicesFactory()
    dealerservice = service_factory.get_instance("dealership")
    dealer = dealerservice.get_dealer_by(dealer_code)
    if dealer:
        if dealer.logo:
            return "<img width='60' src='%s'/> %s" % (dealer.logo.url,dealer.name)
        else:
            return "%s" % dealer.name
    else:
        return ""


@register.simple_tag
def dealer_title_tag(dealer_code):
    service_factory = DealerShipServicesFactory()
    dealerservice = service_factory.get_instance("dealership")
    dealer = dealerservice.get_dealer_by(dealer_code)
    if dealer:
        return dealer.name
    else:
        return ""

@register.simple_tag(takes_context=True)
def dealer_title(context):
        print  "context"
        print context
        try:
            request = context["request"]
            service_factory = DealerShipServicesFactory()
            dealerservice = service_factory.get_instance("dealership")
            if request.session.get("dealer_code",None): 
                dealer = dealerservice.get_dealer_by(request.session["dealer_code"])
            else:
                dealer  = None
                
            if dealer:
                return dealer.name
            else:
                return ""
        except Exception,e:
            return ""
    
    
@register.simple_tag(takes_context=True)
def dealer_detail(context):
    try:
        request = context["request"]
        service_factory = DealerShipServicesFactory()
        dealerservice = service_factory.get_instance("dealership")
        if request.session.get("dealer_code",None): 
            dealer = dealerservice.get_dealer_by(request.session["dealer_code"])
        else:
            dealer  = None
            
        if dealer:
            if dealer.logo:
                return "<img width='60' src='%s'/> %s" % (dealer.logo.url,dealer.name)
            else:
                return "%s" % dealer.name
        else:
             return ""
    except Exception,e:
        return ""

@register.filter(name='checkinnotes')
def checkinnotes(ro):

    note = Notes.objects.filter(ro=ro)
    return  True if len(note) > 0 else False



@register.filter(name='getroinspectionfields')
def getroinspectionfields(params,roNumber):
    
    try:
        print roNumber + "  ," + params
    
        inspection,field =params.split(",")
        roInspection = RoInspection.objects.filter(ro__ro_number = roNumber,inspection__id = inspection)[0]
        x =  eval("roInspection."+field)
        return x
    except Exception as e:
        print e
        return ""
@register.filter(name='strconcat')
def strconcat(str1,str2):
    return str(str1) + "," +str2 

@register.filter(name='generatehtml')   
def generatehtml(param):
    t = Template(param)
    c = Context() 
    return  t.render(c)
@register.filter(name='getColor')
def getColor(roNumber):
    return RoServices().getColorForRO(roNumber)
@register.filter(name='getFlagTimeLapsed')
def getFlagTimeLapsed(ro,flag):
    try:   
        timeLapsed = 0
        if flag == "flag1" and ro.flag1 !=None:
            
                timeLapsed =  timezone.now() - ro.flag1_updated_time
            
        if flag == "flag2" and ro.flag2 !=None: 
            
                timeLapsed =  timezone.now() - ro.flag2_updated_time
            
        result = ""
        if isinstance(timeLapsed, timedelta):
            days = timeLapsed.days
            if days != 0:
                seconds = timeLapsed.seconds
                hours = seconds/60/60
                result = str(days) + "D " + str(hours)+"H"
            else:
                result = str(timeLapsed.seconds/60) +"M" if timeLapsed.seconds/60/60 == 0 else str(timeLapsed.seconds/60/60) + "H"
        return result
    except Exception as e :
        return ""

@register.filter(name='getDivColors')
def getDivColors(status):
    html_class = "alert alert-success"
    try:
      
        if status == "pass":
            html_class = "alert alert-success"
        elif status == "fail":
            html_class = "alert alert-danger"
        elif status == "warning":
            html_class = "alert alert-warning"
    except Exception as e:
            html_class = "alert alert-success"
    return html_class
@register.filter(name='getColorAbr')
def getColorAbr(s):
    return s.upper()
@register.filter(name='getInspectionStatus')
def getInspectionStatus(ro):
    inspection = RoInspection.objects.filter(ro = ro)
    return "Required" if len(inspection) < 1 else "Completed"


@register.filter(name='getModalName')
def getModalName(flag):
    dealer = Dealer.objects.get(id=flag.dealer_id)
    if flag.id == dealer.approval_needed_flag_id:
        return "approvalModal"
    return "flaggingModal"
@register.filter(name="get_object")
def get_object(object):
    print "here"
    print object
            