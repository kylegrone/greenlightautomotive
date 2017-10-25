'''
Created on Nov 29, 2015

@author: mjnasir
'''
from base64 import b64decode
from datetime import datetime, timedelta, date
import pytz
import robotparser

from django.core.files.base import ContentFile
from django.db.models import Q

from dealership.models import  *
from dealership.views.appointment import appointment
from django.utils.timezone import get_current_timezone
from django.utils import timezone
#from macerrors import appIsDaemon
class RoServices():
    def __init__(self,*arg):
        self.dealer = ""
        if len(arg) > 0:
            dealer_id = arg[0]
            self.dealer = Dealer.objects.filter(id = dealer_id)
            if len(self.dealer) > 0:
                self.dealer = self.dealer[0]
      
        

    def getRos(self,dict):
        
        try:
            appointment = Appointment.objects.exclude(ro__isnull = True).filter(dealer= self.dealer)
            if "ro_number" in dict:
                appointment = appointment.filter(ro__ro_number__icontains=dict["ro_number"])
            elif "advisor" in dict:
                appointment = appointment.filter(advisor__userprofile__first_name__icontains=dict["advisor"])
            elif "flags" in dict:
                appointment = appointment.filter(Q(ro__flag1__name__icontains=dict["flags"]) | Q(ro__flag2__name__icontains=dict["flags"]) | Q(ro__flag3__name__icontains=dict["flags"]) )
            if "status" in dict:
                status = True if dict["status"] =="active" else False
#                 ro = RO.objects.filter(ro_status__icontains=status)
                appointment = appointment.filter(ro__ro_status=status)
            if "orderBy" in dict:
                
                order = ""
                if "order" in dict:
                    order = "-" if dict["order"] == "desc" else "" 
                
                sorting = {
                   "ro_number" : order + "ro__ro_number",
                   "ro_date"   : order + "ro__ro_date",
                   "rfid_tag"      : order + "ro__rfid_tag",
                   "customer"  : order + "customer__user__first_name",
                   "year"      : order + "vehicle__vehicle__year__name",
                   "make"      : order + "vehicle__vehicle__make__name", 
                   "model"  : order + "vehicle__vehicle__model__name",
                   "odometer" : order + "vehicle__milage",
                   "advisor"  : order + "advisor__userprofile__first_name",
                   "inspector" : order + "ro__inspector__userprofile__first_name"
                        }    
                appointment= appointment.order_by(sorting[dict["orderBy"]])
            return appointment
        except Exception as e : 
            print e
    def getAllFlagsDealer(self,dealer_id):
        flags1 = Flags.objects.filter(type=1,dealer_id=dealer_id)
        flags2 = Flags.objects.filter(type=2,dealer_id=dealer_id)
        flags3 = Flags.objects.filter(type=3,dealer_id=dealer_id)
        flags = {"flag1" : flags1,
                 "flag2" : flags2,
                 "flag3" : flags3
                 }
        return flags
    def getAllFlags(self):
        flags1 = Flags.objects.filter(type=1)
        flags2 = Flags.objects.filter(type=2)
        flags3 = Flags.objects.filter(type=3)
        flags = {"flag1" : flags1,
                 "flag2" : flags2,
                 "flag3" : flags3
                 }
        return flags
    def get_updated_flags_appointment(self,request):
        dict = request.GET
        flag = False
        updated_flag_id = ""
        updated_flag_time = ""
        if "roId" and "flagId" and "flagType" in dict:
            ro = RO.objects.get(id=dict.get("roId"))
            updated_flag_id = Flags.objects.get(id=dict.get("flagId"))
            updated_flag_time = timezone.now()
            if dict.get("flagType") == "f1":
                flag = True
                ro.flag1 = updated_flag_id
                ro.flag1_updated_time = updated_flag_time
                ro.flag1_updated_by = request.user
            if dict.get("flagType") == "f2":
                flag = True
                ro.flag2 = updated_flag_id
                ro.flag2_updated_time = updated_flag_time
                ro.flag2_updated_by = request.user
            if dict.get("flagType") == "f3" :
                flag = True
                ro.flag3 = updated_flag_id
                ro.flag3_updated_time = updated_flag_time
                ro.flag3_updated_by = request.user
            ro.shop_notes = ""
            if "notes" in dict:
                ro.shop_notes = dict.get("notes")
            
                
            if flag:
                ro.save()
                FlagsHistory(ro = ro , flag = updated_flag_id , created_at = updated_flag_time, created_by = request.user,notes= ro.shop_notes ).save()
                return Appointment.objects.get(ro = ro)
            else:
                return None
       
    def getShopNotes(self,dict):
        
        notes = None
        try:
            if "roId" in dict:
                apt = Appointment.objects.get(ro__id =int(dict.get("roId")),dealer = self.dealer)
                roObject = apt.ro 
#                 roObject = RO.objects.get(id=)
                notes = Notes.objects.filter(ro__id = int(dict.get("roId"))).order_by("-created_at")
            if "ro_number" in dict:
                apt = Appointment.objects.get(ro__ro_number = (dict.get("ro_number")),dealer = self.dealer)
                roObject = apt.ro
#                 roObject = RO.objects.get(ro_number=(dict.get("ro_number")))
                notes = Notes.objects.filter(ro__ro_number=(dict.get("ro_number"))).order_by("-created_at")
            return  notes,roObject
        except Exception as e:
            return None,None
        
        
    def addNote(self,dict,userObj):
        roId = dict.get("roId")
        comment = dict.get("comment")
        
        note = Notes()
        
        note.comment = comment
        
        note.ro = RO.objects.get(id=roId)
        
        note.created_by =  userObj.userprofile
        
        note.current_flag = self.getCurrentFlag(note.ro)
        
        note.save()
        
        return self.getShopNotes({"roId" : roId})
    
    
    def getCustomerServiceRequest(self,requestDict):
        ''' Method to fetch data against RoNumber for TechView '''
        try:
            if "roNumber" in requestDict:
#                 ro = RO.objects.filter(ro_number=requestDict.get("roNumber"))
                
                appointment = Appointment.objects.filter(ro__ro_number = requestDict.get("roNumber"),dealer = self.dealer)
                
                appointmentService = AppointmentService.objects.filter(appointment=appointment)
                total = 0
                 
                
                for ser in appointmentService:
                    serviceDictionary = {}
                    total = total + ser.price
                if len(appointmentService) == 0:
                    return { }
                return {"appointmentService" : appointmentService,"total": total}
           
        except Exception as e:
            print e
        return {} 
            
    def getColorForRO(self,roNumber):
#         try:
        ro = RO.objects.get(ro_number = roNumber)
        flag_colors = [0,0,0]
        max = ro.flag1
        max_time = ro.flag1_updated_time if ro.flag1_updated_time !=None else datetime.datetime(1970,01,01,tzinfo=get_current_timezone())
        import time
        if ro.flag2_updated_time!=None and ro.flag2_updated_time > max_time:
            max = ro.flag2
            max_time = ro.flag2_updated_time
        if  ro.flag3_updated_time!=None and ro.flag3_updated_time > max_time:
            max = ro.flag3
            max_time = ro.flag3_updated_time
        if max !=None:
            return max.color
        return "#FFFFFF"
    def getROdetails(self,roNumber):
        
        try:
            if  roNumber != "":
                appointment = Appointment.objects.get(ro__ro_number=roNumber,dealer = self.dealer)
                userObj = { "roNumber" : roNumber,
                           "vin" : appointment.vehicle.vin_number,
                            "owner" : appointment.customer.first_name +appointment.customer.last_name ,
                            "phone" : appointment.customer.phone_number_1,
                           }
                
                return userObj
        except Exception as e:
            return None
    def getCustomerInspectionRecommendation(self,roNumber):
        try:
            
            if roNumber != "":
                appointment = Appointment.objects.get(ro__ro_number=roNumber,dealer = self.dealer)
                
                aptInspection = AppointmentRecommendation.objects.filter(appointment = appointment)
                
                approvedTotal = 0
                
                declinedTotal = 0
                
                for ins in aptInspection:
                    if ins.status and  ins.status.lower() == "decline":
                        declinedTotal = declinedTotal + ins.price
                    if ins.status and ins.status.lower() == "accept":
                        approvedTotal = approvedTotal + ins.price
                if len(aptInspection) > 0:
                    return {"recommendation":aptInspection,"approved" : approvedTotal , "declined" : declinedTotal ,"total":approvedTotal+declinedTotal} 
        except Exception as e:
            pass
        return {}
    def getAllInspectionObjects(self,roNumber):
        params={}
        params["tire"] = self.getInspectionObjectByCategory("Tire" ,roNumber)
        params["windsheilds"] = self.getInspectionObjectByCategory("Windsheild",roNumber)
        params["components"] = self.getInspectionObjectByCategory("Components",roNumber)
        params["fluids"] = self.getInspectionObjectByCategory("Fluids",roNumber)
        params["lights"] = self.getInspectionObjectByCategory("Lights",roNumber)
        return params
        
    def getInspectionObjectByCategory(self,category,roNumber):
        
#         ro = RO.objects.filter(roNumber=roNumber)
        apt = Appointment.objects.filter(ro__ro_number = roNumber, dealer = self.dealer)
        if len(apt) > 0 :
            return InspectionCatagories.objects.filter(Q(ro__isnull=True) | Q(ro__ro_number = roNumber),type=category)
        return []
    def processInspectionFields(self,request):
        post_request = request.POST
        ro_number = request.POST.get("ro_number")
        
        category_items_dict = {}
        try:
            ro = RO.objects.get(ro_number=ro_number)
            ro.inspector = request.user
            ro.inspection_status = "Completed"
            ro.save()
            for key,value in post_request.iteritems():
                if key == "ro_number" or key == "package":
                    continue
                attr,category_id,item_id = key.split("_")
                if category_id +"_" +item_id in category_items_dict:
                    category_items_dict[category_id + "_" + item_id][attr] = value
                else:
                    category_items_dict[category_id + "_" + item_id] = {attr : value}
            for key,value in category_items_dict.iteritems():
                category_id,item_id = key.split("_")
                category_item = InspectionCategoriesItems.objects.get(category__id = category_id ,item__id = item_id)
                ro_inspection = RoInspection.objects.filter(inspection = category_item,ro = ro)
                if len(ro_inspection) < 1:
                    ro_inspection = RoInspection()
                    ro_inspection.inspection = category_item
                    ro_inspection.ro = ro
                else:
                    ro_inspection = ro_inspection[0]
                for attr,val in value.iteritems():
                    if attr == "image":
                        import uuid
                        val = ContentFile(b64decode(val.split(",")[1]), uuid.uuid1().hex +".png")
                    ro_inspection.__setattr__(attr,val)
                ro_inspection.save()
                     
#         postRequset = request.POST
#         user = request.user  
#         post_dict ={}
# #         print request.POST
#         try:
#             for key,value in postRequset.iteritems():
#                 if key =="roNumber":
#                     continue
#                 id,val =key.split("_")[1:]
#                 if int(id) in post_dict:
#                     post_dict.get(int(id)).update({val : value})
#                 else:
#                     post_dict[int(id)] = {val : value}
#             self.getInspectionCategoriesObjectsById(post_dict)
#             self.saveRoInspection(post_dict,postRequset.get("roNumber"),user)
        except Exception as e:
            print e
    def getInspectionCategoriesObjectsById(self,list): 
        for id in list:
#             objectDictionary[id] = InspectionCatagories(id=id)
            list.get(id).update({"inspection" : InspectionCatagories(id=id)  })
#     def getTiresInspection(self,roNumber):
#         pass
#     def getFluidInspection(self,roNumber):
#         pass    
#     def getWindSheild(self,roNumber):
#         pass
#     def getComponents(self,roNumber):
#         pass
    def saveRoInspection(self,dict,roNumber,user):
        ro = RO.objects.get(ro_number = roNumber)
#         RoInspection.objects.filter(ro=ro).delete()
        for key,value in dict.iteritems():
            try:
                roInspection = RoInspection.objects.get(ro=ro,inspection=value["inspection"])
            except :
                roInspection = RoInspection()
            for name,val in value.iteritems():
#                 str = "roInspection." + name + "=" +"val"
#                 eval(str)
            
                if name == "status":
                    roInspection.status = val
                if name == "recommendation":
                    roInspection.recommendations = val
                if name == "observation":
                    roInspection.observation = val
                if name == "specs":
                    roInspection.specs = val
                if name == "image":
                    image_data = b64decode(val.split(",")[1])
                    import uuid
                    roInspection.image = ContentFile(image_data, uuid.uuid1().hex +".png")
                if name == "inspection":
                    roInspection.inspection = val
            roInspection.ro = ro
            
            roInspection.inspector = user
            roInspection.save()
        ro.inspector = user
        ro.inspection_status = "Completed"
        ro.save()
    def getImagesByRoNumber(self,roNumber):
        try:
            images=[]
            apt = Appointment.objects.get(ro__ro_number = roNumber)
            ro  = apt.ro
            roInspections = RoInspection.objects.filter(ro = ro)
            for roInspection in roInspections:
                if roInspection.image !="":
                    images.append(roInspection)
            return images
        except Exception as e:
           print e
           return []
                
    def deleteImage(self,request):            
        roNumber = request.GET.get("roNumber")
        id = request.GET.get("id")
        model = RoInspection if request.GET.get("type") == "inspection" else walkaroundnotes
        try:
            obj = model.objects.get(id=id)
            obj.image = ""
            obj.save()
        except Exception as e:
            print e 
    def getCurrentFlag(self,ro):
        sum = 1
        if ro.flag1 !=None:
            sum = 1
            if ro.flag2 !=None:
                sum =2 
                if ro.flag3 !=None:
                    sum = 3
        return "flag" + str(sum)
    
    
    def getFlagToUpdateType(self,roId):
        try:
            ro = RO.objects.get(pk=int(roId))
            flagToUpdated = "flag1"
            if ro.flag1 !=None:
                flagToUpdated = "flag2"
                if ro.flag2 !=None:
                    flagToUpdated = "flag3"
                    if ro.flag3 !=None:
                        flagToupdated = "none"
            return flagToUpdated
        except Exception as e:
            print e
     
    def getSummaryDetailsByRoNumber(self,roNumber,package=None):
        o = RoInspection.objects.filter(ro__ro_number = roNumber)
        try:
            if package is not None:
                o = o.filter(inspection__category__package__package = package) 
        
        except Exception,e:
            pass
        return o
   
    
    
    def getTimeLapsed(self,ro,flag): 
        try:   
            timeLapsed = 0
            if flag == "flag1" and ro.flag1 !=None:
                
                    timeLapsed =  timezone.now() - ro.flag1_updated_time
                
            if flag == "flag2" and ro.flag2 !=None: 
               
                    timeLapsed =  timezone.now() - ro.flag2_updated_time
               
            if flag == "flag3" and ro.flag3 !=None:
                    
                    timeLapsed =  timezone.now() - ro.flag2_updated_time
            return timeLapsed
        except Exception as e :
            return ""
    def getRoleOfUser(self,user):
        role = user.groups.all()
        roleString = ""
        for r in role:
            roleString +=r.name + ","
        return roleString
    
    def getInspectionRecommendationSummary(self,roNumber):
        try:
            apt = AppointmentRecommendation.objects.filter(appointment__ro__ro_number = roNumber)
            return apt
        except Exception as e:
            return []
        
    def getWalkAroundImages(self,roNumber):
        images = []
        try:
            walkArounds = walkaroundnotes.objects.filter(appointment__ro__ro_number = roNumber , appointment__dealer = self.dealer)
            for walkAround in walkArounds:
                if walkAround.image != "" and walkAround.image !=None:
                    images.append(walkAround)
            return images
        except Exception as e :
            return  []
    def addRecommendations(self,request):
        dict = {}
        roId = request.GET.get("roId")
        user = request.user
        for key,value in request.GET.iteritems():
            if "_" in key:
                id = key.split("_")[0]
                name = key.split("_")[1]
                if id in dict:
                    dict[id].update({ name : value})
                else:
                    dict[id] = { name : value }
        print dict
        self.addServiceRepair(dict,roId,user)
    def addServiceRepair(self,dict,roId,user):
        try:
            apt = Appointment.objects.get(ro__id=roId)
            for key,value in dict.iteritems():
                try:
                    recommendation  =  AppointmentRecommendation()
                    notes = ""
                    price = 0
                    for name,val in value.iteritems():
                        
                        if name == "name":
                            recommendation.name = val
                        if name == "labor":
                            recommendation.labor = float(val)
                            price+=float(val)
                        if name == "parts":
                            recommendation.parts = float(val)
                            price+=float(val)
                        if name == "notes":
                            recommendation.notes = val
                    recommendation.price =price
                    recommendation.appointment= apt
                    recommendation.price_unit =apt.dealer.price_unit
                    recommendation.save()
#                     ser.price = float(ser.labor) + float(ser.parts)
#                     ser.dealer_id = apt.dealer_id
#                     ser.save()
#                     AppointmentRecommendation(appointment = apt,service=N,recommnded_by=user,notes=notes).save()
                except Exception,e:
                    print e
        except Exception,e:
            print e
    
    
    
    def get_inspection_data(self,ro_number,package,dealer_id):
        try:
            package = InspectionPackage.objects.get(package=package,dealer = self.dealer)
            categories = InspectionCatagories.objects.filter(package = package)
            categories_items = InspectionCategoriesItems.objects.filter(category__in=categories)
            categories_items_dict= {}
            for category_item in categories_items:
                ro_inspection = RoInspection.objects.filter(inspection=category_item,ro__ro_number = ro_number)
                ro_inspection_dict = {"recommendation":"","observation":"","specs":"","status":"pass"}
                if len(ro_inspection) > 0:
                        ro_inspection = ro_inspection[0]
                        ro_inspection_dict = {"recommendation":ro_inspection.recommendations,"observation":ro_inspection.observation,"specs" :ro_inspection.specs,"status":ro_inspection.status}
                    
                if category_item.category in categories_items_dict:
                         
                    categories_items_dict[category_item.category][category_item.item]= ro_inspection_dict
                else:
                    categories_items_dict[category_item.category] = {category_item.item : ro_inspection_dict}
            return categories_items_dict
        except Exception,e :
            return {}
    
    def get_all_packages(self):
        return InspectionPackage.objects.filter(dealer=self.dealer)
    
class Reports():
        def __init__(self,*arg):
            self.dealer = ""
            if len(arg) > 0:
                dealer_id = arg[0]
                self.dealer = Dealer.objects.filter(id = dealer_id)
                if len(self.dealer) > 0:
                    self.dealer = self.dealer[0]
        def get_repair_order_list(self,ro_number,start_date,end_date):
            all_ro = Appointment.objects.filter(ro__isnull=False,dealer = self.dealer)
            if ro_number != "":
                all_ro = all_ro.filter(ro__ro_number= ro_number)
            if start_date !="":
    #             all_ro = all_ro.filter()
                pass
            
            report = []
            
            
            
            for apt in all_ro:
                ro = apt.ro
                report_row = {}
                report_row["ro_number"] = ro.ro_number
                report_row["ro_closed_date"] = (ro.ro_completed if ro.ro_completed !=None else "")
                report_row["eligible_closed_ro"] = ("Yes" if ro.ro_completed !=None else "No")
                report_row["requested_inpsection"] = "Yes"
                report_row["inpsection"] = ("Yes" if ro.inspection_status !="Required" else "No")
                report_row["tech"] = ro.inspector.first_name + "," + ro.inspector.last_name if ro.inspector else ""
#                 apt = Appointment.objects.get(ro__ro_number = ro.ro_number)
                report_row["vehicle"] =apt.vehicle.vehicle.make.name
                report_row["milage"] = apt.vehicle.milage
                apt_recommendatin = AppointmentRecommendation.objects.filter(appointment=apt)
                report_row["num_of_tech_inspections"] = apt_recommendatin.count()
                fail = apt_recommendatin.filter(result="fail").select_related("service")
                
                failed_dollars = map(lambda f :f.service.price ,fail)
                
                report_row["failed_recs_price"] = sum(failed_dollars)
                
                accepted = apt_recommendatin.filter(status="Accept")
                
                report_row["accepted_dollars"]  = sum(map(lambda f : f.service.price ,accepted))
                report_row["upsell_ro"] = sum(map(lambda f: f.service.price,apt_recommendatin))
                report.append(report_row)
                
            return report
        
        
        def get_service_advisor_report(self):
            all_appointments = Appointment.objects.filter(dealer= self.dealer)
            advisors = set(map(lambda app :app.advisor,all_appointments ))
            report = []
            for advisor in advisors:
                row = {}
                row["advisor"] = "%s %s" % (advisor.first_name,advisor.last_name)
                row["closed_ros"] = Appointment.objects.filter(advisor = advisor,ro__ro_completed__isnull=False,dealer=self.dealer).count()
                closed_ro = Appointment.objects.filter(advisor = advisor,ro__ro_completed__isnull=False)
                if row["closed_ros"] != 0:
                    row["average_milage"]=sum(map(lambda f:f.vehicle.milage,closed_ro))/row["closed_ros"]
                else:
                    row["average_milage"] = 0
                rec_inpsection = closed_ro.filter(ro__inspection_status ="Required")
                rec_closed_ro=closed_ro.filter(ro__inspection_status ="Completed")
                total = rec_inpsection.count() + rec_closed_ro.count()
                if total !=0:
                    row["rec_inpsection"] = (rec_inpsection.count()*100)/total
                    row["rec_closed_ro"] = (rec_closed_ro.count()*100)/total
                else:
                    row["rec_inpsection"] = 0
                    row["rec_closed_ro"] = 0
                apt = Appointment.objects.filter(advisor = advisor,dealer=self.dealer)
                ro = map(lambda f:f.ro,apt)
                if len(ro) !=0:
                    row["tec_recs_per_inspection"] = RoInspection.objects.filter(ro__in=ro).count() / len(ro)
                else:
                    row["tec_recs_per_inspection"] = 0
                report.append(row)
            return report
                
        def get_technician_analysis_report(self):
            
            all_ro = RO.objects.all()
            inspectors = map(lambda f:f.inspector,all_ro)
            inspectors = set(inspectors)
            report = []
            for inspector in inspectors:
                rows = {}
                ros = RO.objects.filter(inspector = inspector)
                rows["technician"] = inspector
                rows["sa_req_inspection"] = RoInspection.objects.filter(ro__in=ros).values("ro").distinct().count()
                rows["req_inspection_completed"] = rows["sa_req_inspection"]
                rows["req_inspection_completed_percent"] = "100%"
                rows["ros_with_inspection"] = RoInspection.objects.filter(ro__in=ros).values("ro").distinct().count()
                all_appointments = Appointment.objects.filter(ro__in = ros)
                rows["milage"] = sum(map(lambda f:f.vehicle.milage,all_appointments))
                rows["tech_recs_per_inspection"] = RoInspection.objects.filter(ro__in=ros).values("ro").distinct().count()/ros.count()
                report.append(rows)
            return report
        def getShopFlagAnalysisReport(self,ro_number):
            try:
                list =[]
                
                aptObjects = Appointment.objects.exclude(ro__isnull = True).filter(dealer=self.dealer)
                if ro_number !="":
                    aptObjects = aptObjects.filter(ro__ro_number = ro_number)
                for apt in aptObjects:
                    if apt.ro.flag1 !=None:
                        list.append({"roNumber" : self.is_null(apt.ro.ro_number),"advisor" : self.is_null(apt.advisor.last_name) + "," + self.is_null(apt.advisor.first_name),"technician" :self.is_null(apt.ro.inspector.last_name) + "," + self.is_null(apt.ro.inspector.first_name),"flagCreator" : self.is_null(apt.ro.flag1_updated_by.last_name) + "," + self.is_null(apt.ro.flag1_updated_by.first_name) ,"flag" : self.is_null(apt.ro.flag1.name),"timeLapsed":self.getTimeLapsed(apt.ro, "flag1"),"flagStarted" : apt.ro.flag1_updated_time,"role":self.getRoleOfUser(apt.ro.flag1_updated_by)})
                    if apt.ro.flag2 !=None:
                        list.append({"roNumber" : self.is_null(apt.ro.ro_number),"advisor" : self.is_null(apt.advisor.last_name) + "," + self.is_null(apt.advisor.first_name),"technician" :self.is_null(apt.ro.inspector.last_name) + "," + self.is_null(apt.ro.inspector.first_name),"flagCreator" : self.is_null(apt.ro.flag2_updated_by.last_name) + "," + self.is_null(apt.ro.flag2_updated_by.first_name) ,"flag" : self.is_null(apt.ro.flag2.name),"timeLapsed":self.getTimeLapsed(apt.ro, "flag2"),"flagStarted" : apt.ro.flag2_updated_time,"role":self.getRoleOfUser(apt.ro.flag1_updated_by)})
                    if apt.ro.flag3 !=None:
                        list.append({"roNumber" : self.is_null(apt.ro.ro_number),"advisor" : self.is_null(apt.advisor.last_name) + "," + self.is_null(apt.advisor.first_name),"technician" :self.is_null(apt.ro.inspector.last_name) + "," + self.is_null(apt.ro.inspector.first_name),"flagCreator" : self.is_null(apt.ro.flag3_updated_by.last_name) + "," + self.is_null(apt.ro.flag3_updated_by.first_name) ,"flag" : self.is_null(apt.ro.flag3.name),"timeLapsed":self.getTimeLapsed(apt.ro, "flag3"),"flagStarted" : apt.ro.flag3_updated_time,"role":self.getRoleOfUser(apt.ro.flag1_updated_by)})
                return list
            except Exception as e:
                print e
                return []       
        def is_null(self,obj):
            return "" if obj == None else obj
        def getTimeLapsed(self,ro,flag): 
            try:   
                timeLapsed = 0
                if flag == "flag1" and ro.flag1 !=None:
                    
                        timeLapsed =  timezone.now() - ro.flag1_updated_time
                    
                if flag == "flag2" and ro.flag2 !=None: 
                   
                        timeLapsed =  timezone.now()- ro.flag2_updated_time
                   
                if flag == "flag3" and ro.flag3 !=None:
                        
                        timeLapsed =  timezone.now() - ro.flag2_updated_time
                return timeLapsed
            except Exception as e :
                return ""
        def getRoleOfUser(self,user):
            role = user.groups.all()
            roleString = ""
            for r in role:
                roleString +=r.name + ","
            return roleString
        def get_selected_package(self):
            
            
            ins = InspectionPackage.objects.filter(dealer=self.dealer)
            if len(ins) > 0:
                
                return ins[0].package
            return ""