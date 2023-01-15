from django.urls import path

from . import views  
 # url attached to methods in view page
#path empty conected to index method in view

urlpatterns=[
    path('',views.index, name='index'),
    path('about',views.about, name='about')
     ]