from datetime import timedelta
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from dealership.factories import DealerShipServicesFactory
from dealership.models import * 


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        dealer_factory = DealerShipServicesFactory()
        appointmentservce = dealer_factory.get_instance("appointment")
        print "here"
        appts = appointmentservce.update_noshow()
        