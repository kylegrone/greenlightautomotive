from datetime import timedelta
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from dealership.factories import DealerShipServicesFactory
from dealership.models import * 


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        dealer_factory = DealerShipServicesFactory()
        capacityservice = dealer_factory.get_instance("capacity")
        dealers =Dealer.objects.all()
        now = datetime.datetime.now()
        start_date = now.date()
        end_date = start_date + timedelta(7)
        for dealer in dealers:
            capacityservice.save_tech_count_for_date_range(start_date,end_date,dealer)
        