from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import service_unavailable
@login_required
@service_unavailable
def searcher(request):
    return render(request, 'search/searcher.html')

@login_required
@service_unavailable
def start(request):
    return render(request, 'search/start.html')