from django import template
from django.core.urlresolvers import reverse

from dealership.factories import DealerShipServicesFactory


register = template.Library()

@register.simple_tag
def dealer_ico(dealer_code):
    service_factory = DealerShipServicesFactory()
    dealerservice = service_factory.get_instance("dealership")
    dealer = dealerservice.get_dealer_by(dealer_code)
    if dealer:
        if dealer.ico_logo:
            
            return "<link rel='shortcut icon' href='%s'/>" % (dealer.ico_logo.url,)
        else:
            return "<link rel='shortcut icon' href='%s' />" % (dealer.ico_logo,)
    else:
        return ""

@register.simple_tag
def dealer_detail(dealer_code):
    service_factory = DealerShipServicesFactory()
    dealerservice = service_factory.get_instance("dealership")
    dealer = dealerservice.get_dealer_by(dealer_code)
    if dealer:
        if dealer.logo:
            return "<img width='60' src='%s'/>&nbsp;&nbsp;%s" % (dealer.logo.url,dealer.name)
        else:
            return "%s" % dealer.name
    else:
        return ""

@register.simple_tag
def dealer_detail_customer(dealer_code):
    service_factory = DealerShipServicesFactory()
    dealerservice = service_factory.get_instance("dealership")
    dealer = dealerservice.get_dealer_by(dealer_code)
    main_url = reverse("customer:main")+"?dealer_code="+dealer_code
    if dealer:
        if dealer.logo:
            return "<a href='%s' class='logo'><h1><img width='60' src='%s'/>&nbsp;&nbsp;%s</h1></a>" % (main_url,dealer.logo.url,dealer.name)
        else:
            return "%s" % dealer.name
    else:
        return ""
    
    
@register.simple_tag
def dealer_detail_dealer(dealer_code):
    service_factory = DealerShipServicesFactory()
    dealerservice = service_factory.get_instance("dealership")
    dealer = dealerservice.get_dealer_by(dealer_code)
    main_url = reverse("dealership:index")+"?dealer_code="+dealer_code
    if dealer:
        if dealer.logo:
            return "<a href='%s' class='logo'><img width='60' src='%s'/>&nbsp;&nbsp;%s DEALERSHIP APPLICATION</a>" % (main_url,dealer.logo.url,dealer.name)
        else:
            return "%s" % dealer.name
    else:
        return ""

@register.simple_tag
def dealer_title(dealer_code):
    service_factory = DealerShipServicesFactory()
    dealerservice = service_factory.get_instance("dealership")
    dealer = dealerservice.get_dealer_by(dealer_code)
    if dealer:
        return dealer.name
    else:
        return ""
