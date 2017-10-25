from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from dealership import conf 
from dealership.decorators import dealer_group_check
from dealership.forms import *
from dealership.services.userservices import UserService
from flagging import Constants
from flagging.decorators import technician_group_check
from flagging.forms import *
from customer.decorators.decorators import dealership_required


# Create your views here.
@user_passes_test(technician_group_check,login_url=Constants.REDIRECT_URL)
def index(request):
    dealer_code = None
    if request.GET.get("dealer_code"):
        dealer_code =request.GET["dealer_code"]
    elif request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    
    template_name = 'flagging/index.html'
    return render(request, template_name,{"dealer_code" : dealer_code})

@dealership_required
def loginview(request,dealer):
    
    dealer_code = dealer
    if request.user.is_authenticated() and request.user.groups.filter(name__in=[Constants.TECHNICIAN]):
        if request.user.last_login is None:
            return HttpResponseRedirect(reverse("flagging:firstlogin")) 
        else:
            return HttpResponseRedirect(reverse("flagging:confirmation"))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None and user.userprofile.dealer.dealer_code == request.session["dealer_code"]:                
                if user.is_active:
                    if technician_group_check(user) == True:
                        if form.cleaned_data['remember'] == True:
                            request.session.set_expiry(0)
                        if user.last_login is None:
                            login(request, user)
                            request.session["dealer_code"] = dealer_code
                            return HttpResponseRedirect(reverse("flagging:firstlogin"))
                        else:
                            login(request, user)
                            request.session["dealer_code"] = dealer_code
                            return HttpResponseRedirect(reverse("flagging:index"))  
                    else:
                        form.add_error("username","not allowed")   
                else:
                    form.add_error("username","user is not active")
            else:
                form.add_error("username","username password incorrect")
    else:
        form = LoginForm()
    template = 'flagging/login.html'
    
    return render(request, template, {'form': form,"dealer_code" : request.session["dealer_code"]})

def logoutview(request):
    dealer_code = request.session["dealer_code"]
    logout(request)
    return HttpResponseRedirect(reverse("flagging:login") + "?dealer_code=" + dealer_code)
                                

@user_passes_test(technician_group_check,login_url=Constants.REDIRECT_URL)
def firstlogin(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    current_user = request.user
    if request.method == 'POST':
        user_service = UserService()
        form = SecretQuestionForm(request.POST)
        if form.is_valid():
            user_service.save_user_pasword_answers(current_user,form.cleaned_data['new'],form.cleaned_data['questions'], form.cleaned_data['answer'])
            messages.success(request, 'Password has been updated. Please provide the new credentials')
            return HttpResponseRedirect(Constants.REDIRECT_URL)
    else:
        #     
        form = SecretQuestionForm()
    template = 'flagging/firstlogin.html'
    return render(request, template, {'form': form,"dealer_code":dealer_code})

@user_passes_test(technician_group_check,login_url=Constants.REDIRECT_URL)
def passchange(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)        
        if form.is_valid():
            return HttpResponseRedirect(reverse("flagging:index"))
    else:
        form = ChangePasswordForm()
    template = 'flagging/password_change.html'
    return render(request, template, {'form': form,"dealer_code":dealer_code})



def passcreate(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    form = CreatePasswordForm()
    template = 'flagging/404.html'
    question = '';
    token = request.GET.get('token')
    if token is not None:
        user_service = UserService()
        user = user_service.get_user_from_token(token)
        if user is not None:
            template = 'flagging/password_create.html'
            question =  user_service.get_user_question(user) 
            if request.method == 'POST':
                form = CreatePasswordForm(request.POST)                   
                if form.is_valid():
                    if user_service.verify_user_answer(user, form.cleaned_data['answer']) == True:
                        user_service.save_user_password(user, form.cleaned_data['new'])
                        messages.success(request, 'Password has been updated. Please provide the new credentials')
                        return HttpResponseRedirect(reverse("flagging:login"))
                    else:
                       form.add_error("answer","You have not provided the correct answer")  
        
    return render(request, template, {'form': form, 'question' : question, 
                                      'token':token,"dealer_code":dealer_code})

def passreset(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    if request.method == 'POST':
        form = ResetForm(request.POST)        
        if form.is_valid():
            try:
                user = User.objects.get(email = form.cleaned_data['email'])                
                user_service = UserService()
                token = user_service.create_token(user)
                try:      
                    user_service.send_pass_reset_link(user, request, "/flagger/password/create")         
                    messages.success(request, 'Email has been sent') 
                    return HttpResponseRedirect(reverse("flagging:login"))                 
                except Exception as e:
                    form.add_error("email","email sending failed")                 
            except Exception, e: 
                print e
                form.add_error("email","email doesnot exist")  
    else:
        form = ResetForm()
    template = 'flagging/password_reset.html'
    return render(request, template, {'form': form,"dealer_code":dealer_code})

def terms(request):
    template_name = 'flagging/terms.html'
    return render(request, template_name)
def userreset(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    if request.method == 'POST':
        form = ResetForm(request.POST)        
        if form.is_valid():
            try:
                user = User.objects.get(email = form.cleaned_data['email'])                
                user_service = UserService()
                try:      
                    user_service.send_username_link(user)           
                    messages.success(request, 'Email has been sent')                 
                except:
                    form.add_error("email","email sending failed")                 
            except: 
                form.add_error("email","email doesnot exist")  
    else:
        form = ResetForm()
    template = 'flagging/username_reset.html'
    return render(request, template, {'form': form,"dealer_code":dealer_code})


def newuser(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    if request.method == "POST":
        form = NewUserEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            userService = UserService()
            try:
                userService.sendEmailToITForCreation(email)
                messages.success(request, 'Email has been sent') 
            except:
                form.add_errors("email","email doesnt exist")
    else:
        form = NewUserEmailForm()
    return render(request, "flagging/newuser.html",{"form" : form,"dealer_code":dealer_code})
@user_passes_test(technician_group_check,login_url=Constants.REDIRECT_URL)
def addTempNumber(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    if request.method == "POST":
        form = TempNumberForm(request.POST)
        loggedInUser = request.user
        try:
            userProfile = UserProfile.objects.get(user=loggedInUser)
            if userProfile:
                userProfile.active_phone_number = request.POST['number']
                userProfile.active_phone_number_date = datetime.now()
                userProfile.save()
                return HttpResponseRedirect(reverse("flagging:index"))
        except Exception,e:
            print e
            pass
    else:
        form = TempNumberForm()
    
    return render(request,"flagging/tempnumber.html",{"form": form,"dealer_code":dealer_code})
@user_passes_test(technician_group_check,login_url=Constants.REDIRECT_URL)
def confirmation(request):
    dealer_code = None
    if request.session.get("dealer_code"):
        dealer_code =request.session["dealer_code"]
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user=current_user)
    if request.method == "POST":
#         form = UpdateNumberOrEmailForm(request.POST)
        type = request.POST.get("modeType")
        if type == "email":
            current_user.email = request.POST.get("field")
            current_user.save()
        elif type == "text":
            current_user_profile.phone_number = request.POST.get("field")
            current_user_profile.save()
        elif type == "skip":
            is_skip = request.POST.get("is_skip_hidden")
        
#
#         is_skip = form.cleaned_data['skip']
            current_user_profile.skip_confirmation = True if is_skip=="true" else False
            current_user_profile.save()
    if request.method == "GET":
        
        if current_user_profile:
            
            if not current_user_profile.skip_confirmation:
                template_name = "flagging/confirmation.html"
                form = UpdateNumberOrEmailForm()
                return render(request,template_name,{"form":form,"userProfile":current_user_profile,"dealer_code":dealer_code})
    
    return HttpResponseRedirect(reverse("flagging:index"))
            
        
        
    
    
    
    
    