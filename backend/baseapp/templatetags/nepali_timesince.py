from django import template
from django.utils.timesince import timesince as _timesince

register = template.Library()


@register.filter
def nepali_timesince(value):
    
    timesince_str = _timesince(value)
    
    # Split on comma and keep only the first part
    timesince_str = timesince_str.split(',')[0]
    translations = {
        "minutes": "मिनेट",
        "hours": "घण्टा",
        "day": "दिन",
        "week": "हप्ता",
        "month": "महिना",
        "year": "वर्ष"
    }
    for eng, nep in translations.items():
        timesince_str = timesince_str.replace(eng, nep)
    return timesince_str
   