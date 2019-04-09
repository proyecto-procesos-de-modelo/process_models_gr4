
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path


from storage_go_app import views as app_views

urlpatterns = [

    # Home
    path('home/', app_views.home, name='home'),

    # Acceso/Registro Urls
    path('acceso', app_views.custom_login, name='custom_login'),
    path('desconectar', app_views.custom_logout, name='custom_logout'),
    path('registro', app_views.custom_register, name='custom_register'),
    path('restablecer_contrasena', app_views.custom_reset_password, name='custom_reset_password'),

]
