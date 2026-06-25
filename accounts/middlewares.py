
from django.http import HttpResponseForbidden
from django.core.cache import cache
class IPBlockerMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
       
    def __call__(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        if ip and cache.get(f"BANNED_IP_{ip}"):
            return HttpResponseForbidden("Your IP is flagged as spam")
        
        response = self.get_response(request)
        return response