import datetime
import time

from django.utils import timezone
import pytz

from BMW import settings
from dealership.models import Dealer, ShopHours, DealerFavorites, Favorites
from django.forms.models import model_to_dict



class DealerShipService():
    
    def setservices(self):
        from dealership.factories import DealerShipServicesFactory
        self.dealer_service_factory = DealerShipServicesFactory()
        self.userservice = self.dealer_service_factory.get_instance("user")        
        self.vehicle_service = self.dealer_service_factory.get_instance("vehicle")
        self.repair_service = self.dealer_service_factory.get_instance("repair")
        self.dealership_service = self.dealer_service_factory.get_instance("dealership")
        self.capacity_service = self.dealer_service_factory.get_instance("capacity")
        self.email_service = self.dealer_service_factory.get_instance("email")
        self.dealership_service = self
    
    def get_dealer_by(self,dealer_code):
        """
                This functiojn is used to get the dealer
        """
        try:
            dealer =  Dealer.objects.get(dealer_code=dealer_code)
            return dealer
        except Exception,e:
#             print str(e)+"Dealer not found"+dealer_code
            return None
        
    def get_dealer_by_id(self,dealer_id):
        """
            this is to get dealer by id
        """
        try:
            dealer =  Dealer.objects.get(id=dealer_id)
            return dealer
        except:
            return None
      
   
              
    def get_dealer_shop_time(self, date, dealer_id):
        time = ShopHours.objects.filter(shop_id = dealer_id, day = date.strftime('%A'))
        if time:
            open_time = datetime.datetime.strptime("%s %s %s %s" %(date.year, date.month, date.day,time[0].time_from), '%Y %m %d %H:%M:%S')
            close_time = datetime.datetime.strptime("%s %s %s %s" %(date.year, date.month, date.day,time[0].time_to), '%Y %m %d %H:%M:%S')
            open_time = timezone.make_aware(open_time)
            close_time =timezone.make_aware(close_time)
            capcity_per = time[0].capacity_percent
            
        else:
            open_time = datetime.datetime.strptime("%s %s %s %s" %(date.year, date.month, date.day,"08:00:00"), '%Y %m %d %H:%M:%S')
            close_time = datetime.datetime.strptime("%s %s %s %s" %(date.year, date.month, date.day,"08:00:00"), '%Y %m %d %H:%M:%S')
            open_time = timezone.make_aware(open_time)
            close_time =timezone.make_aware(close_time)
            capcity_per=100
        return {'open_time':open_time,
                    'open_time_string':open_time.strftime('%Y-%m-%d %H:%M'),                    
                    'close_time': close_time,
                    'close_time_string':close_time.strftime('%Y-%m-%d %H:%M'),
                    'slot': 20,"on":True,"capacity":capcity_per}  
            
     
    def get_all_favorites(self):
        self.setservices()
        favorites_list = []
        try:
            favorites = Favorites.objects.all()               
            favorites_list = list(favorites.values())
        except Exception as ex:
            self.email_service.send_exception("dealership", 
                                          "DealerShipService", 
                                          "get_dealer_favorites", 
                                          str(ex));
        return favorites_list
    
    def save_dealer_favorites(self, dealer_id, favorites_id):
        favorites  = DealerFavorites()
        favorites.dealer_id = dealer_id
        favorites.favorites_id = favorites_id
        favorites.save()
        
    def get_dealer_favorites(self, dealer_id):
        self.setservices()
        favorites_list = []
        try:
            favorites = DealerFavorites.objects.filter(dealer_id = dealer_id)
            for fav in favorites:            
                favorites_list.append({"id":fav.id,
                                       "name": fav.favorites.name,
                                       "url_name": fav.favorites.url_name,
                                       "url_qstring": fav.favorites.url_qstring})            
        except Exception as ex:
            self.email_service.send_exception("dealership", 
                                          "DealerShipService", 
                                          "get_dealer_favorites", 
                                          str(ex));
        return favorites_list
        