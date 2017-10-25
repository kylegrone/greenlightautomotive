from customer.services.accountservice import AccountService
from customer.services.cameraservice import CameraService
from customer.services.userservices import CUserService


class CustomerServicesFactory(object):
    def get_instance(self,name):
        if name=="user":
            return CUserService()
        elif name == "account":
            return AccountService()
        elif name == "camera":
            return CameraService()
    