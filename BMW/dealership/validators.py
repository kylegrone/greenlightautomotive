from django.core.exceptions import ValidationError

def validate_phone(value):
    if value % 2 != 0:
        raise ValidationError('%s is not an even number' % value)