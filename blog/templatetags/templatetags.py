from django import template

register = template.Library()

# a filter to replace args with ***
 
@register.filter()
def replace_with_asterisk(value,args):
    return value.replace(args,"***")

@register.filter()
def split_with_space(value):
    return value.split(" ")

