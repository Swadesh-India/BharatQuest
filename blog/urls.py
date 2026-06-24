from django.urls import path

from . import views

urlpatterns=[
path('', views.blogs, name='blogs'),
path('<int:blog_id>/<slug:slug>/', views.blog_detail, name='blog_detail'),
path('add_blog/', views.add_blog, name='add_blog'),
path('edit_blog/', views.edit_blog, name='edit_blog'),
path("myblogs/",views.myblogs, name="myblogs"),
    ]