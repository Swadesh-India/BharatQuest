from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages
def service_unavailable(func):
    
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        messages.error(request,"503, Service Unavailable")
        return redirect("service-unavailable")
    return wrapper