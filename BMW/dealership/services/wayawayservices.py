'''
Created on Dec 21, 2015

@author: aroofi
'''
from dealership.models import *

class WayAwayService():
    
    def get_all_wayaway(self,dealer=None):
        wayaways = WayAway.objects.all()
        wayaway_array = []
        for wayaway in wayaways:
            wayaway_tmp = {"dealer":None,"default":wayaway}
            if dealer:
                try:
                    wayaway_tmp["dealer"] = WayAwayDealer.objects.get(dealer=dealer,wayaway=wayaway)
                except Exception,e:
                    print e
            wayaway_array.append(wayaway_tmp)
        return wayaway_array 
    
    def get_apt_wayaway(self, appt):
        try:
            app = Appointment.objects.get(id=appt)
            return app.way_away_id
        except Exception,e:
            print e
            return None
        
        
    def update_wayaway(self,appt , wayaway,driver_liscens_number=None,insurance_company_name=None,insurance_card_number=None,state_id=None,reserve=0):
        if appt and wayaway:
            try:
                app = Appointment.objects.get(id=appt)
                app.way_away_id = wayaway
                app.driver_liscens_number = driver_liscens_number
                app.insurance_company_name = insurance_company_name
                app.insurance_card_number = insurance_card_number
                app.state_wayaway_id = state_id
                app.reserve_wayaway = reserve
                app.save()
            except Appointment.DoesNotExist:
                return False
        
        
        return True
    
    
    def get_all_states(self):
        states = States.objects.all()
        return states