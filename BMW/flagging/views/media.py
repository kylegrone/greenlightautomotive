'''
Created on Jan 5, 2016

@author: mjnasir
'''


from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from dealership.models import RoInspection
from flagging.services.RoServices import RoServices
#from flagging.factory import RoServicesFactory


def media(request):
    params = {}
    if request.method == "GET":
        if "roNumber" in request.GET :
            roNumber = request.GET.get("roNumber")
            roService = RoServices(request.session["dealer_id"])
            params["roDetails"] = roService.getROdetails(roNumber)
            params["color"] = roService.getColorForRO(roNumber)
            params["images"] = roService.getImagesByRoNumber(roNumber)
            params["walkArounds"] = roService.getWalkAroundImages(roNumber)
            params["roNumber"] = roNumber            
    
    
    return render(request,"flagging_app/media.html",params)


def delete_media(request):
    if request.method == "GET":
        
        roService = RoServices()
        roService.deleteImage(request)
        return HttpResponseRedirect( reverse('flagging:media')+"?roNumber=" +request.GET.get("roNumber") )