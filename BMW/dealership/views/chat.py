from django import forms
from django.conf import settings
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
from livechat.forms import UploadForm
from livechat.services.channels import ChannelService


# @user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
def chats(request):
    service = ChannelService()
    template_name = 'dealership/chats/index.html'
    channels = service.get_all_channels(request.user.id)

    img=UploadForm()
   
    context = {"CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
                                          "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET,
                                        "advisor":request.user,
                                             
                                             "channels":channels,
#                                            "advisor":user,
                                         'imgform':img,}
    return render(request, template_name,context)


# @user_passes_test(dealer_group_check,login_url=conf.REDIRECT_URL)
def chat(request):
    service = ChannelService()
    template_name = 'dealership/chats/singlechat.html'
    channel = None
    img=UploadForm()
    
    if request.GET.get("chat_id"):
        channel =service.get_chat(request.GET.get("chat_id"))
    elif request.GET.get("channel") and request.GET.get("advisor") and request.GET.get("guest_user") :
        channel = service.getchannel(request.GET["channel"],request.GET["guest_user"],request.GET["advisor"])
        
    context = {"CENTRIFUGE_URL":settings.CENTRIFUGE_URL,
                                          "CENTRIFUGE_SECRET":settings.CENTRIFUGE_SECRET,
                                        "advisor":request.user,
#                                              "advisor":user,
                                          
                                         'form':img,"channel":channel}
    return render(request, template_name,context)

