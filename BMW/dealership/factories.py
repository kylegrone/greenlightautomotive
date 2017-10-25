from dealership.services.appointmentservices import AppointmentService
from dealership.services.dealershipservice import DealerShipService
from dealership.services.notificationservice import NotificationService
from dealership.services.repairservices import RepairService
from dealership.services.userservices import UserService
from dealership.services.vehicleservices import VehicleService
from dealership.services.wayawayservices import WayAwayService
from dealership.services.capacityservice import CapacityService
from dealership.services.emailservice import EmailService


# from dealership.services.notifiationservice import NotificationService
class DealerShipServicesFactory(object):
    def get_instance(self,name):
        if name=="user":
            return UserService()
        elif name == "vehicle":
            return VehicleService()
        elif name == "dealership":
            return DealerShipService()
        elif name =="repair":
            return RepairService()
        elif name == "appointment":
            return AppointmentService()
        elif name == "wayaway":
            return WayAwayService()
        elif name == "notification":
            return NotificationService()
        elif name=="capacity":
            return CapacityService()
        elif name=="email":
            return EmailService()