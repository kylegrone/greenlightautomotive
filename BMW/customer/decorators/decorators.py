from functools import wraps

from django.http.response import HttpResponseRedirect, Http404

from customer.app_confg import confg
from django.contrib.auth import logout as auth_logout
from customer.services.userservices import CUserService
from dealership.services import appointmentservices
from dealership.services.dealershipservice import DealerShipService


def customer_group_check(user):
    if not user.groups.filter(name__in=[confg.GROUP_NAME]):
        return False
    return True


def customer_not_group_check(user):
    if not user.is_authenticated() and not user.groups.filter(name__in=[confg.GROUP_NAME]):
        return False
    return True

def resetlogin(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
#         auth_logout(request)
        return f(request,*args, **kwargs)
    return wrap

def dealership_required(f):
        
        @wraps(f)
        def wrap(request, *args, **kwargs):
                dealer_code = None
                if request.method =="POST" and request.POST.get("dealer_code"):
                    dealer_code = request.POST.get("dealer_code") 
                elif kwargs.get("dealer_code"):
                    dealer_code = kwargs["dealer_code"]
                    kwargs.pop("dealer_code")
                elif request.GET.get("dealer_code"):
                    dealer_code =request.GET.get("dealer_code")
                elif request.session  and request.session.get("dealer_code"):
                    dealer_code =request.session.get("dealer_code") 
                      
                dealer_service = DealerShipService()
                dealership = dealer_service.get_dealer_by(dealer_code)
                #this check the session if userid key exist, if not it will redirect to login page
                
                if request.session and request.session.get("dealer_code") and dealer_code !=request.session.get("dealer_code"):
                    """if the dealer in the session is different then in the request logging out the user"""
                    print "logging out the user"
                    auth_logout(request)
                    
                if dealership == None:
                        raise Http404("Please access a valid dealer portal")
                else:
                    request.session["dealer_code"] = dealer_code
                    request.session["dealer_name"] = dealership.name
                    request.session["dealer_id"] = dealership.id
                
                return f(request, dealer_code,*args, **kwargs)
        return wrap


def appointment_required(f):
        @wraps(f)
        def wrap(request, *args, **kwargs):
                appservice  = appointmentservices.AppointmentService()
                appointment_id = None
                
                if request.method =="POST":
                    appointment_id = request.POST.get("appointment_id")
                      
                if appointment_id == None:
                    appointment_id =request.GET.get("appointment_id")   
                
                appointment = appservice.get_valid_appointment(appointment_id)
                #this check the session if userid key exist, if not it will redirect to login page
                if appointment == None:
                        raise Http404("Appointment does not exist")
                else:
                    request.session["appointment_id"] = appointment_id
                return f(request, appointment,*args, **kwargs)
        return wrap


def dealership_required_or_logged_in(f):
        @wraps(f)
        def wrap(request, *args, **kwargs):
                userservice = CUserService()
                user = request.user
                profile = None
                dealer_code = None
                if  user and user.is_authenticated() and  user.groups.filter(name__in=[confg.GROUP_NAME]):
                    dealer_code =request.session["dealer_code"]
                    profile = user.userprofile
                else: #if user not logged in
                    if request.GET.get("profile_id")!=None:
                        profile = userservice.get_user_profile(request.GET.get("profile_id"))
                    if request.method =="POST" and request.POST.get("dealer_code"):
                        dealer_code = request.POST.get("dealer_code")
                    elif kwargs.get("dealer_code"):
                        dealer_code = kwargs["dealer_code"]
                        kwargs.pop("dealer_code")
                    elif request.GET.get("dealer_code"):
                        dealer_code =request.GET.get("dealer_code")
                    elif request.session  and request.session.get("dealer_code"):
                        dealer_code =request.session.get("dealer_code")
                    
                    if request.session and request.session.get("dealer_code") and dealer_code !=request.session.get("dealer_code"):
                        """if the dealer in the session is different then in the request logging out the user"""
                        auth_logout(request)
                       
                    dealer_service = DealerShipService()
                    dealership = dealer_service.get_dealer_by(dealer_code)
                    #this check the session if userid key exist, if not it will redirect to login page
                    if dealership == None:
                            raise Http404("Please access a valid dealer portal")
                    else:
                        request.session["dealer_code"] = dealer_code
                return f(request, dealer_code,profile,*args, **kwargs)
        return wrap


 

 
