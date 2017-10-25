from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from mobilecheckin import confg
from mobilecheckin.decorators import *
from dealership.forms import *
from dealership.services.userservices import UserService
from customer.decorators.decorators import dealership_required

# Create your views here.

""" 
    Dealerhip Login View
    *Contains all the view related to dealer's account management
"""

login_template = 'mobilecheckin/login/'
base_template = 'mobilecheckin/'


@dealership_required
def loginview(request,dealer_code=None): 
    """
    LoginView
    * confrims if user is not logged in already
    * verify username and password and check if user belongs to the group dealership
    * checks user firstlogin
    * checks if dealer has signed the terms
    """ 
    
    if request.user.is_authenticated() and request.user.groups.filter(name__in=[confg.GROUP_NAME]):
        if request.user.userprofile.terms_agreed == 'True':
            return HttpResponseRedirect(reverse('mobilecheckin:index'))
        else:
            return HttpResponseRedirect(reverse('mobilecheckin:terms'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None and user.userprofile.dealer.dealer_code == request.session["dealer_code"]:                
                if user.is_active:
                    for g in user.groups.all():
                        if g.name == confg.ADVISOR_GROUP_NAME or g.name == confg.GROUP_NAME:
                            request.session["group"] = g.name                              
                            if user.last_login is None:
                                login(request, user)
                                request.session["dealer_code"] = dealer_code
                                return HttpResponseRedirect(reverse('mobilecheckin:firstlogin'))
                            else:
                                login(request, user)
                                request.session["dealer_code"] = dealer_code
                                if form.cleaned_data['remember'] == True:
                                    request.session.set_expiry(259200000)
                                if user.userprofile.terms_agreed == 'False':                                
                                    return HttpResponseRedirect(reverse('mobilecheckin:terms'))
                                else:
                                    return HttpResponseRedirect(reverse('mobilecheckin:index'))  
                        else:
                            form.add_error("username",confg.LOGIN_USERNAME_ERROR)   
                else:
                    form.add_error("username",confg.LOGIN_USERNAME_ACTIVE_ERROR)
            else:
                form.add_error("username",confg.LOGIN_USERNAME_INCORRECT_ERROR)
    else:
        form = LoginForm()
    template = login_template+'login.html'
    return render(request, template, {'form': form,"name":request.session["dealer_name"],
                                      "code":request.session["dealer_code"],'dealer_code':request.session["dealer_code"]})

def requestview(request):
    """
    RequestView
    *Gets the email from user and sends it to IT for creating account
    """
    if request.method == 'POST':
        form = ResetForm(request.POST)        
        if form.is_valid():
            email = form.cleaned_data['email']
            user_service = UserService()
            try:                
                user = User.objects.get(email = email, groups__name = confg.GROUP_NAME) 
            except:
                user = None
            
            if user is None: 
                try:      
                    user_service.send_account_request(email)           
                    messages.success(request, confg.REQUEST_EMAIL_SENT_MESSAGE)                 
                except:
                    form.add_error("email",confg.REQUEST_EMAIL_SENT_ERROR)                 
            else: 
                form.add_error("email",confg.REQUEST_EMAIL_EXIST_ERROR)  
    else:
        form = ResetForm()
    template = login_template+'request.html'
    return render(request, template, {'form': form,"code":request.session["dealer_code"]})

def logoutview(request):
    """
    LogoutView
    *Log out user
    """
    dealer_code = request.session["dealer_code"]
    logout(request)
    return HttpResponseRedirect(reverse('mobilecheckin:login')+"?dealer_code="+dealer_code)  

@user_passes_test(checkin_group_check,login_url=confg.REDIRECT_URL)
def firstlogin(request):
    """
    FirstLoginView
    * asks the user to create password
    * get security question from user
    * redirect to terms on success
    """
    current_user = request.user
    dealer_code = request.session["dealer_code"]
    if request.method == 'POST':
        user_service = UserService()
        form = SecretQuestionForm(request.POST)
        if form.is_valid():
            print "i am mobile checkin"
            user_service.save_user_pasword_answers(current_user,form.cleaned_data['new'],form.cleaned_data['questions'], form.cleaned_data['answer'])
            messages.success(request, confg.FIRSTLOGIN_MESSAGE)
            return HttpResponseRedirect((reverse('mobilecheckin:login')+"?dealer_code="+dealer_code))
    else:     
        form = SecretQuestionForm()
    template = login_template+'firstlogin.html'
    return render(request, template, {'form': form,"code":request.session["dealer_code"]})

@user_passes_test(checkin_allow_check,login_url=confg.REDIRECT_URL)
def passchange(request):
    """
    PassChange
    * change user password
    """
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)   
        dealer_code = request.session["dealer_code"]
        if form.is_valid():
            user = request.user
            print user
            user_service = UserService()
            if user.check_password(form.cleaned_data['current']) == True:
                user_service.save_user_password(user, form.cleaned_data['new'])
                messages.success(request, confg.PASSCHANGE_MESSAGE)
                return HttpResponseRedirect((reverse('mobilecheckin:login')+"?dealer_code="+dealer_code))
            else:
                form.add_error("current",confg.PASSCHANGE_CURRENT_ERROR) 
    else:
        form = ChangePasswordForm()
    template = login_template+'password_change.html'
    return render(request, template, {'form': form,"code":request.session["dealer_code"]})



def passcreate(request):
    """
    PassCreate
    * create user password on password reset request
    """
    form = CreatePasswordForm()
    template = base_template+'404.html'
    question = '';
    token = request.GET.get('token')
    if token is not None:
        user_service = UserService()
        user = user_service.get_user_from_token(token)
        dealer_code = request.session.get("dealer_code","")    
        if user is not None:
            template = login_template+'password_create.html'
            question =  user_service.get_user_question(user) 
            if request.method == 'POST':
                form = CreatePasswordForm(request.POST)                   
                if form.is_valid():
                    if user_service.verify_user_answer(user, form.cleaned_data['answer']) == True:
                        user_service.save_user_password(user, form.cleaned_data['new'])
                        messages.success(request, confg.PASSCREATE_MESSAGE)
                        return HttpResponseRedirect((reverse('mobilecheckin:login')+"?dealer_code="+dealer_code))
                    else:
                        form.add_error("answer",confg.PASSCREATE_ANSWER_ERROR)  
        
    return render(request, template, {'form': form, 'question' : question, 'token':token,"code":request.session["dealer_code"]})

def passreset(request):
    """
    PassCreate
    * Request for creating new password
    """
    if request.method == 'POST':
        form = ResetForm(request.POST)        
        if form.is_valid():
            try:
                user = User.objects.get(email = form.cleaned_data['email'] , groups__name = confg.GROUP_NAME)  
                if checkin_access_check(user) == False:
                    form.add_error("email",confg.RESET_EMAIL_GROUP_ERROR)   
                else:              
                    user_service = UserService()                      
                    try:      
                        user_service.send_pass_reset_link(user, request, "/mobilecheckin/password/create")           
                        messages.success(request, confg.RESET_EMAIL_SENT_MESSAGE)                
                    except:
                        form.add_error("email",confg.RESET_EMAIL_SENT_ERROR)                 
            except: 
                form.add_error("email",confg.RESET_EMAIL_EXIST_ERROR)  
    else:
        form = ResetForm()
    template = login_template+'password_reset.html'
    return render(request, template, {'form': form,"code":request.session["dealer_code"]})

def userreset(request):
    """
    UserReset
    * Request to retrieve username
    """
    if request.method == 'POST':
        form = ResetForm(request.POST)        
        if form.is_valid():
            try:
                user = User.objects.get(email = form.cleaned_data['email'], groups__name = confg.GROUP_NAME) 
                if checkin_group_check(user) == False:
                    form.add_error("email",confg.RESET_EMAIL_GROUP_ERROR)   
                else:
                    user_service = UserService()
                    try:      
                        user_service.send_username_link(user)           
                        messages.success(request,  confg.RESET_EMAIL_SENT_MESSAGE)                 
                    except:
                        form.add_error("email",confg.RESET_EMAIL_SENT_ERROR)                 
            except: 
                form.add_error("email",confg.RESET_EMAIL_EXIST_ERROR)  
    else:
        form = ResetForm()
    template = login_template+'username_reset.html'
    return render(request, template, {'form': form,"code":request.session["dealer_code"]})

#@user_passes_test(dealer_group_check,login_url=confg.REDIRECT_URL)
@checkin_access_check
def terms(request):
    """
    UserReset
    * Present dealer with terms to sign
    """
    if request.method == 'POST':
        currentuser = request.user
        currentuser.userprofile.terms_agreed = True
        currentuser.userprofile.save()
        return HttpResponseRedirect(reverse('mobilecheckin:index'))
    template_name = login_template+'terms.html'
    return render(request, template_name)

