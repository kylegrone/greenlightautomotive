from django.core.urlresolvers import reverse_lazy


GROUP_NAME = "Customer"
REDIRECT_URL = reverse_lazy("customer:index")
SESSION_MAKE_KEY = "vehicle_make"
SESSION_YEAR_KEY = "vehicle_year"
SESSION_VIN_NUM_KEY = "vehicle_vin_number"
ADVISOR_GROUP_NAME = "Advisor"