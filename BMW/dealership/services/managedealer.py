from dealership.models import *



class ManageDealer():
        
    def getdetail(self,dealer_id):
        dealer = Dealer.objects.get(id=dealer_id)
        return dealer
    
    def getcontacts(self,dealer_id):
        contacts = ShopsContact.objects.filter(shop_id = dealer_id)
        return contacts
    
    def getcontactsbyid(self,contact_id):
        contact = ShopsContact.objects.get(id = contact_id)
        return contact
    
    def getotheremails(self,dealer_id ,type):
        emails = ShopOtherEmails.objects.filter(shop_id = dealer_id , type = type)
        
        return emails
    def getotheremailbyid(self,id):
        email = ShopOtherEmails.objects.get(id=id)
        return email
    
    def getsmsno(self,dealer_id):
        sms = ShopSMS.objects.filter(shop_id = dealer_id)
        return sms
    
    def getsmsnobyid(self,sms_id):
        sms = ShopSMS.objects.get(id = sms_id)
        return sms
    
    def getshophrs(self,dealer_id):
        hrs = ShopHours.objects.filter(shop_id = dealer_id)
        return hrs
    
    def getshophrsbyid(self,sh_id):
        hr = ShopHours.objects.get(id = sh_id)
        return hr
    
    def getholidays(self,dealer_id):
        holiday = ShopHolidays.objects.filter(shop_id = dealer_id)
        return holiday
    
    def getholidaybyid(self,hl_id):
        holiday = ShopHolidays.objects.get(id = hl_id)
        return holiday
    
    def updateconatcts(self,dealer_id , updated_date):
        ShopsContact.objects.filter(shop_id = dealer_id , updated_date__lt = updated_date).delete()
        ShopOtherEmails.objects.filter(shop_id = dealer_id , updated_date__lt = updated_date).delete()
        ShopSMS.objects.filter(shop_id = dealer_id , update_date__lt = updated_date).delete()
        ShopHolidays.objects.filter(shop_id = dealer_id , updated_date__lt = updated_date).delete()
        
    def getamenities(self,dealer_id):
        amenities_id = []
        amenities = ShopAmenities.objects.filter(shop_id = dealer_id)
        for obj in amenities:
            amenities_id.append(obj.amenities_id)
        return amenities_id
   
    def set_Restrictiondays(self , obj , days):
        if 7 not in days:
            if 1 in days:
                obj.monday = 1
            else:
                obj.monday = 0
            if 2 in days:
                obj.tuesday = 1
            else:
                obj.tuesday = 0
            if 3 in days:
                obj.wednesday = 1
            else:
                obj.wednesday = 0
            if 4 in days:
                obj.thursday = 1
            else:
                obj.thursday = 0
            if 5 in days:
                obj.friday = 1
            else:
                obj.friday = 0
            if 6 in days:
                obj.saturday = 1
            else:
                obj.saturday = 0
        else:
            obj.monday = 1
            obj.tuesday = 1
            obj.wednesday = 1
            obj.thursday = 1
            obj.friday = 1
            obj.saturday = 1
        obj.save()
            
    def get_user_profile_details(self,id):
        user = UserProfile.objects.get(user_id = id)
        team = TeamAdvisors.objects.filter(advisor_id = id)
        teamids = []
        for t in team:
            teamids.append(t.team_id.id)
        grp_id = ""
        if user.user.groups.all():
            grp_id = user.user.groups.all()[0].id
        return {'first': user.first_name, 'last':  user.last_name, 'email': user.email_1 ,'phone1': user.phone_number_1,'phone2':user.phone_number_2,
                'employee':user.employee_no,'role': grp_id ,'team':teamids,'reserve':"",'username':user.user.username, 'password':user.user.password,
                'image':user.avatar , 'reserve' : int(user.consumer_reserver) , 'user_id':user.user.id}
    
    
    def get_capacity(self,id):
        cap = ""
        try:
            cap = AdvisorCapacity.objects.get(advisor_id = id)
            cap.monday = int(cap.monday)
            cap.tuesday = int(cap.tuesday)
            cap.wednesday = int(cap.wednesday)
            cap.thursday = int(cap.thursday)
            cap.friday = int(cap.friday)
            cap.saturday = int(cap.saturday)
        except AdvisorCapacity.DoesNotExist:
            pass
        return cap
    
    def get_restrictions(self,id):
        rest = AdvisorRestrictions.objects.filter(advisor_id = id)
        for rst in rest:
            days=[]
            if rst.monday and rst.tuesday and rst.wednesday and rst.thursday and rst.friday and rst.saturday :
                days.append(7)
            else:
                if rst.monday:
                    days.append(1)
                if rst.tuesday:
                    days.append(2)
                if rst.wednesday:
                    days.append(3)
                if rst.thursday:
                    days.append(4)
                if rst.friday:
                    days.append(5)
                if rst.saturday:
                    days.append(6)
            if rst.start_time == None:
                rst.start_time = ""
            if rst.end_time == None:
                rst.end_time = ""
            if rst.end_date == None:
                rst.end_date=""
            if rst.start_date == None:
                rst.start_date =""
            rst.days = days
            rst.repeat = int(rst.repeat)
        return rest
    
    def get_flag_data_bydealer(self,type,dealer_id):
        flags = Flags.objects.filter(type = type,dealer_id=dealer_id)
        flist = []
        for obj in flags:
            fdic= {"value" : str(obj.id) , "label": str(obj.name) , "type": str(obj.type) , "cfacing": str(obj.customer_facing) , "notes" : str(obj.notes) , "color" : str(obj.color),"approval_required": str(self.is_approval_required_flag(dealer_id) == obj.id).lower() }
            flist.append(fdic)
        
        return flist
    def get_flag_data(self,type,dealer_id):
        flags = Flags.objects.filter(type = type,dealer_id = dealer_id)
        flist = []
        for obj in flags:
            fdic= {"value" : str(obj.id) , "label": str(obj.name) , "type": str(obj.type) , "cfacing": str(obj.customer_facing) , "notes" : str(obj.notes) , "color" : str(obj.color),"approval_required": str(self.is_approval_required_flag(dealer_id) == obj.id).lower() }
            flist.append(fdic)
        
        return flist
    def is_approval_required_flag(self,dealer_id):
        try:
           return  Dealer.objects.get(id = dealer_id).approval_needed_flag_id
        except  Exception as e:
            return -1