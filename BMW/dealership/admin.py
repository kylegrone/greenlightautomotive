from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from dealership.models import *


# Register your models here.
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fk_name = 'user'
    verbose_name_plural = 'User Profile'
    exclude = ['active_email','active_email_date','active_phone_number','active_phone_number_date',
               'phone_number_2', 'phone_number_3', 'phone_1_type', 'phone_2_type', 'phone_3_type',
               'email_1', 'email_2', 'state_us',
               'terms_agreed','token','token_expiry','number_of_chats','skip_confirmation'
               'mode_of_sending_updates',"question","answer","mode_of_sending_updates","skip_confirmation"]



# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    
class VehicleAdmin(admin.ModelAdmin):
    pass




class DealerVehicleAdmin(admin.ModelAdmin):
    pass

class DealerAdmin(admin.ModelAdmin):
    pass
class AppointmentAdmin(admin.ModelAdmin):
    pass

class FlagsAdmin(admin.ModelAdmin):
    pass
class RoAdmin(admin.ModelAdmin):
    pass

class CustomerVehicleAdmin(admin.ModelAdmin):

    pass

class DealerServicesAdmin(admin.ModelAdmin):
    pass
class AppointmentServiceAdmin(admin.ModelAdmin):
    pass
class AppointmentRecommendationAdmin(admin.ModelAdmin):
    pass
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Vehicle,VehicleAdmin)
admin.site.register(DealersVehicle, DealerVehicleAdmin)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Dealer,DealerAdmin)

admin.site.register(Flags,FlagsAdmin)
admin.site.register(RO, RoAdmin)
admin.site.register(CustomerVehicle,CustomerVehicleAdmin)
admin.site.register(ServiceRepair,DealerServicesAdmin)
admin.site.register(AppointmentService,AppointmentServiceAdmin)
admin.site.register(AppointmentRecommendation,AppointmentRecommendationAdmin)
