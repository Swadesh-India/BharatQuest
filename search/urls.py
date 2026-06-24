from django.urls import path

from . import views

urlpatterns =[
            path('', views.searcher, name='searcher'),
    
    path('results/', views.start, name='results'),
    ]