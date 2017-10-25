from django.core.urlresolvers import reverse

class BreadCrumb():  

    dictionary = {
             "overview":{"name":"Today's Overview", 'url':"overview", "q":""},
             "appointment":{"name":"Appointment", 'url':"appointment", "q":""},
             "customers":{"name":"Customers", 'url':"customers", "q":""},
             "rservices":{"name":"Services & Repairs", 'url':"rservices", "q":""},
             "manage":{"name":"Dealership", 'url':"manage", "q":""},
             "ov_time_daily_time":{"name":"Day View", 'url':"ov_time_daily", "q":"?q=time"},
             "ov_time_daily_advisor":{"name":"Advisor View", 'url':"ov_time_daily", "q":"?q=advisor"},
             "ov_time_daily_status":{"name":"Status View", 'url':"ov_time_daily", "q":"?q=status"},
             "ov_time_weekly_time":{"name":"Week View", 'url':"ov_time_weekly", "q":"?q=time"}, 
             "ov_time_weekly_advisor":{"name":"Advisor Week View", 'url':"ov_time_weekly", "q":"?q=advisor"}, 
             "ov_time_weekly_status":{"name":"Status Week View", 'url':"ov_time_weekly", "q":"?q=status"} 
    }
    
    def create_breadcrumb(self, items):
        breadcrumb = []
        for item in items:
            breadcrumb.append({'name':self.dictionary[item]['name'], 'url':reverse('dealership:%s' % (self.dictionary[item]['url']))})
        
        return breadcrumb