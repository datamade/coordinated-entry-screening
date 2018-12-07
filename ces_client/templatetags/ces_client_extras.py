from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_settings_value(setting_variable):
    return getattr(settings, setting_variable, '')