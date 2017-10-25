from django import template

register = template.Library()



@register.filter(name='checkincounter')
def checkincounter(item, arg):
    print item,arg
    if item%arg == 0:
        return True
    else:
        return False


