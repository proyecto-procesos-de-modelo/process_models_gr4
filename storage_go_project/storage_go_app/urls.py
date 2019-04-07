
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path


from storage_go_app import views as app_views
from storage_go_app import models as app_models

urlpatterns = [

    # Home
    path('home/', app_views.home, name='home'),

    # Acceso/Registro Urls
    path('acceso', app_views.custom_login, name='custom_login'),
    path('desconectar', app_views.custom_logout, name='custom_logout'),
    path('registro', app_views.custom_register, name='custom_register'),
    path('restablecer_contrasena', app_views.custom_reset_password, name='custom_reset_password'),

    # Map Urls
    path('mapa',
        app_views.map.as_view(),
        name='map_stadistics'),

   
    # Move Tasks Urls


    path('tareas/',
        app_views.CustomListView.as_view(
            model=app_models.MoveTask),
        name='task_list'),

    path('tareas/crear',
        app_views.CustomCreateView.as_view(
            model=app_models.MoveTask),
        name='task_create'),

    path('tareas/<int:id>/editar',
        app_views.CustomUpdateView.as_view(
            model=app_models.MoveTask),
        name='task_update'),

    path('tareas/<int:id>/ver',
        app_views.CustomDetailView.as_view(
            model=app_models.MoveTask),
        name='task_view'),

    path('tareas/<int:id>/borrar',
        app_views.CustomDeleteView.as_view(
            model=app_models.MoveTask),
        name='task_delete'),

    # Maintenance Task Tasks Urls

    # Products Urls

    # Containeres Urls

    #Room Urls
     path('room/<int:id>/view',
        app_views.CustomDetailView.as_view(model=app_models.Room),
        name='room_view'),
]
