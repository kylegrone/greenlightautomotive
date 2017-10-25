import django.utils.timezone
from django.http.response import Http404

from dealership.services.dealershipservice import DealerShipService


class TimeZoneMiddleware(object):
    # Check if client IP is allowed
    def process_request(self, request):
                if request.method =="POST" and request.POST.get("dealer_code"):
                    dealer_code = request.POST.get("dealer_code")  
                else:
                    dealer_code =request.GET.get("dealer_code")   
                    if dealer_code ==None:
                        dealer_code = request.session.get("dealer_code")
                if dealer_code:
                    dealer_service = DealerShipService()
                    dealership = dealer_service.get_dealer_by(dealer_code)
                    if dealership and dealership.timezone:
                        try:
                           
                            django.utils.timezone.activate(dealership.timezone)
                        except Exception,e:
                            print "Error setting timezone",e
               
              