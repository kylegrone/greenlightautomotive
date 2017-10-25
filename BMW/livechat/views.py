from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import request
from django.utils.crypto import get_random_string

from customer.decorators.decorators import dealership_required_or_logged_in
from customer.factories import CustomerServicesFactory
from dealership.factories import DealerShipServicesFactory
from dealership.services.userservices import UserService
from livechat.forms import UploadForm
from livechat.models import Upload
from livechat.services.channels import ChannelService


@dealership_required_or_logged_in
def index(request,dealer_code,profile):
    """    
            this method is the index view for the chat session. Its just a test page currently 
            for advisors
    """
    customer_factory = CustomerServicesFactory()
    dealer_factory = DealerShipServicesFactory()
    dealer_service = dealer_factory.get_instance("dealership")#DealerShipService()
    dealership = dealer_service.get_dealer_by(dealer_code)
    userservice = customer_factory.get_instance("user")#CUserService()
   
#     userservice = UserService()
    advisor = userservice.get_advisor_for_chat(dealership,profile)
    img=UploadForm()
    template_name = 'livechat/advisorchat.html'
    chat_username = getUserName(request)
    chat_nick = getChatNick(request)
    
    return render(request, template_name,{"CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
                                          "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET,
                                          "advisor":advisor,"chat_username":chat_username,"chat_nick":chat_nick
                                         ,'form':img })
    
    
def upload(request):
    """    
           This method is used to upload the images of the chat and save it to a model.
    """
    resp = {"success":False,"imgurl":None}
    if request.method=="POST":
        img = UploadForm(request.POST, request.FILES)       
        if img.is_valid():
            imgfieds = img.save()  
#             
            resp["success"] = True
            resp["imgurl"] = imgfieds.pic.url
            return JsonResponse(resp)
    return JsonResponse(resp)
#   

def addchannel(request):
    """    
            This method is used to add channel( chat session)
    
    """
    channelservice = ChannelService()
    resp = False
    if request.GET.get("channel") and request.GET.get("advisor") and request.GET.get("guest_user") :
        resp = channelservice.saveChanneldForAdvisor(request.GET["channel"],request.GET["guest_user"],request.GET["advisor"])
        channelservice.add_chat_count(request.GET.get("advisor"))
    return JsonResponse({"success":resp})



def deleteChannel(request):
    """    
            This method is used to add delete channel( chat session)
    
    """
    channelservice = ChannelService()
    resp = False
    if request.GET.get("channel") and request.GET.get("advisor") and request.GET.get("guest_user") :
        resp = channelservice.deleteChannel(request.GET["channel"],request.GET["guest_user"],request.GET["advisor"])
        channelservice.delete_chat_count(request.GET.get("advisor"))
    return JsonResponse({"success":resp})



def getUserName(request):
    """    
            This method is used to get the username for a logged in user or a guest user
    
    """
    if request.user.is_authenticated():
        return request.user.username
    else:
        if "guest_id" in request.session:
            return request.session["guest_id"]
        else:
            request.session["guest_id"] = "GUEST"+get_random_string()
            return request.session["guest_id"]
        
def getChatNick(request):
    """    
            This method is used to get the nickname for a logged in user or a guest user
    
    """
    if request.user.is_authenticated():
        return request.user.username
    else:
        return "Guest"
    
