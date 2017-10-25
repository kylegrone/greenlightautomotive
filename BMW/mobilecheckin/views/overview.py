'''
Created on Dec 4, 2015

@author: aroofi
'''
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import resolve

from dealership import conf
from dealership.decorators import dealer_group_check
from dealership.forms import *
from dealership.services.appointmentservices import AppointmentService

def overview(request):
    searchform = SearchCustomerForm()
    aptservice = AppointmentService()
    breadcrumb = ["Today's Overview", "Daily View"]
    meters = aptservice.get_meters_data()
    template = 'overview/index.html'
    return render(request, template, {'breadcrumb':breadcrumb, 'meters':meters, 'searchform':searchform})

def ov_time_daily(request):
    template = 'mobilecheckin/appointments/time_daily.html'
    return render(request, template)

def ov_adv_daily(request):
    template = 'overview/adv_daily.html'
    return render(request, template)

def ov_status_daily(request):
    template = 'overview/status_daily.html'
    return render(request, template)

def ov_time_weekly(request):
    template = 'overview/time_weekly.html'
    return render(request, template)

def ov_adv_weekly(request):
    template = 'overview/adv_weekly.html'
    return render(request, template)

def ov_status_weekly(request):
    template = 'overview/status_weekly.html'
    return render(request, template)

def meters_ajax_view(request):
    aptservice = AppointmentService()
    meters = aptservice.get_meters_data()
    template = 'dealership/app/meters.html'
    return render(request, template, {'meters':meters})

def searchcustomer_ajax_view(request):
    template = 'overview/appointment.html'
    context = {}
    if request.method == 'POST':        
        form = SearchCustomerForm(request.POST) 
        if form.is_valid():    
            context  = {}     
    return render(request, template, context)

def dailyapt_ajax_view(request):
    template = 'mobilecheckin/appointments/time_daily_slab.html'
    context = {}
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = aptservice.get_appoiontments_by_time(request.POST.get('year'),request.POST.get('month'),request.POST.get('day'),request.POST.get('hour'),request.POST.get('minute'))      
           
    return render(request, template, context)

def advisor_daily_slab_ajax_view(request):
    template = 'mobilecheckin/appointments/time_daily_slab.html'
    context = {}
    print "new function "
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = aptservice.get_appointments_by_advisor(request.POST.get('year'),request.POST.get('month'),request.POST.get('day'),request.POST.get('id'), request.POST.get('title'))      
        print context   
    return render(request, template, context)

def status_daily_slab_ajax_view(request):
    template = 'mobilecheckin/appointments/time_daily_slab.html'
    context = {}
    print "new function "
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = aptservice.get_appointments_by_status(request.POST.get('year'),request.POST.get('month'),request.POST.get('day'),request.POST.get('id'), request.POST.get('title'))      
        print context   
    return render(request, template, context)

def time_weekly_slab_ajax_view(request):
    template = 'mobilecheckin/appoinments/time_weekly_slab.html'
    context = {}
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = aptservice.get_appoiontments_by_time(request.POST.get('year'),request.POST.get('month'),request.POST.get('day'),request.POST.get('hour'),request.POST.get('minute'))      
        context["id"] = request.POST.get('id')
    return render(request, template, context)

def appointment_row_ajax_view(request):
    template = 'mobilecheckin/appoinments/time_daily_row.html'
    context = {}
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = {'row':aptservice.get_appointment_by_id(request.POST.get('id'))}    
        print context
    return render(request, template, context)

def time_weekly_day_ajax_view(request):
    template = 'mobilecheckin/appoinments/time_weekly_day.html'
    context = {}
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = aptservice.get_appointments_day(request.POST.get('year'),request.POST.get('month'),request.POST.get('day'))      
        context['id'] = request.POST.get('id')    
    return render(request, template, context)

def appointment_detail_ajax_view(request):
    template = 'mobilecheckin/appointments/detail.html'
    context = {}
    if request.method == 'POST': 
        aptservice = AppointmentService()
        id = request.POST.get('id')
        print id
        row  = aptservice.get_appointment_by_id(id)
        context = {"id": request.POST.get('id'), "row": row }#aptservice.get_appointment_by_id(request.POST.get('id'));     
    return render(request, template, context)
    
def advisor_ajax_view(request):
    #template = 'overview/daily_slab.html'
    context = {}
    #print "old function "
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = aptservice.get_appointments_advisor()     
        #context['id'] = request.POST.get('id')    
    #return render(request, template, context)
    return JsonResponse(context)

def status_ajax_view(request):
    context = {}
    if request.method == 'POST': 
        aptservice = AppointmentService()
        context = aptservice.get_appointments_status()     
    return JsonResponse(context)