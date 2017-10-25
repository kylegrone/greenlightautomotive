'''
Created on 12-Feb-2016

@author: Shoaib Anwar
'''

from functools import wraps
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from dealership import conf

def checkin_access_check(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        group_name = ""
        if "dealer_code" not in request.session:
            return HttpResponseRedirect(reverse('mobilecheckin:login')) 
        else:
            try:
                group_name = request.session["group"]
            except:
                for g in request.user.groups.all():
                    group_name = g.name
                    request.session["group"] = g.name
            if group_name in [conf.ADVISOR_GROUP_NAME , conf.GROUP_NAME] and request.user.userprofile.dealer.dealer_code == request.session["dealer_code"]:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('mobilecheckin:logout'))        
                 
    return wrap


def checkin_group_check(user):
    if not user.groups.filter(name__in=[conf.ADVISOR_GROUP_NAME]):
        return False
    return True



def checkin_allow_check(user):
    if not user.groups.filter(name__in=[conf.ADVISOR_GROUP_NAME]):
        return False    
    if user.userprofile.terms_agreed == 'False':
        return False   
    return True