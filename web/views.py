from django.shortcuts import render
from django.templatetags.static import static

def service_unavailable_view(request):
    return render(request,"service-unavailable.html")



