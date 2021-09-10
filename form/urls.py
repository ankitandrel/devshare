from django.urls import path
from . import views
urlpatterns = [
    path('submit_resource/', views.submit_resource,name='submit_resource'),
    path('contact_form/', views.contact_form, name='contact_form')
]
