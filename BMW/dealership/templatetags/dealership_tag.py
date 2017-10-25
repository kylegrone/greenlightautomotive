from django import template
from dealership.models import Dealer


register = template.Library()

@register.filter(name='checkinlist')
def checkinlist(item, arg):
    print arg , item
    desired_array = [int(numeric_string) for numeric_string in item]
    return arg in desired_array