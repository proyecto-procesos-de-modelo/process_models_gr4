
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from storage_go_app import views as app_views
from storage_go_app import models as app_models

from storage_go_project import settings


urlpatterns = [

    # General urls
    path('', app_views.home, name='home'),

    path('acceso/', app_views.custom_login, name='custom_login'),
    path('desconectar/', auth_views.LogoutView.as_view(), name='logout'),

    path('activacion/<uidb64>/<token>/', app_views.activation, name='activation'),
    path('password_reset/', app_views.password_reset, name='password_reset'),
    path('password_reset_form/<uidb64>/<token>/', app_views.password_reset_form, name='password_reset_form'),

    # Map Urls
    path('mapa', app_views.map, name='map'),
    path('mapa/estadisticas', app_views.map_statistics, name='map_stadistics'),

    # Move Tasks Urls
    # CustomListView
    path('tareas/',
        app_views.CustomCreateView.as_view(
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

    # Room
    # CustomListView
    path('room/',
        app_views.CustomCreateView.as_view(
            model=app_models.Room),
        name='room_list'),


    path('room/crear',
        app_views.CustomCreateView.as_view(
            model=app_models.Room),
        name='room_create'),

    path('room/<int:id>/editar',
        app_views.CustomUpdateView.as_view(
            model=app_models.Room),
        name='room_update'),

    path('room/<int:id>/ver',
        app_views.CustomDetailView.as_view(
            model=app_models.Room),
        name='room_view'),

    path('room/<int:id>/borrar',
        app_views.CustomDeleteView.as_view(
            model=app_models.Room),
        name='room_delete'),

    # Maintenance Tasks Urls

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




#
