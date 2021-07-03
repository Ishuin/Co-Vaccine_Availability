from django.urls import path
from . import views

urlpatterns = [
    path('', views.Availability.as_view(), name='get'),
    path('form/', views.form_handle, name='form_handle'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-slots/', views.load_slots, name='ajax_load_slots'),
]