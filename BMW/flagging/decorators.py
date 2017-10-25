'''
Created on Nov 18, 2015

@author: mjnasir
'''

from django.core.urlresolvers import reverse
from . import Constants
from django.http import HttpResponseRedirect
from functools import wraps

def technician_group_check(user):
    if user.groups.filter(name__in=[Constants.TECHNICIAN,Constants.ADVISOR,Constants.DEALER]):
        return True
    return False


def flagger_access_check(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        group_name = ""
        if "dealer_code" not in request.session:
            return HttpResponseRedirect(reverse('flagging:login')) 
        else:
            try:
                group_name = request.session["group"]
            except:
                for g in request.user.groups.all():
                    group_name = g.name
                    request.session["group"] = g.name
                 
            if group_name in [Constants.TECHNICIAN,Constants.ADVISOR,Constants.DEALER] and request.user.userprofile.dealer.dealer_code == request.session["dealer_code"]:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('flagging:logout'))
                       
    return wrap