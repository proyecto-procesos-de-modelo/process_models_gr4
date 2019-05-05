
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.views.generic import RedirectView

from storage_go_app import views as app_views
from storage_go_app import models as app_models

from storage_go_project import settings


urlpatterns = [

    # General urls
    #path('', app_views.home, name='home'),
    path('', RedirectView.as_view(url='/panel/mapa/')),

    path('acceso/', app_views.custom_login, name='custom_login'),
    path('desconectar/', auth_views.LogoutView.as_view(), name='logout'),
    path('activacion/<uidb64>/<token>/', app_views.activation, name='activation'),
    path('password_reset/', app_views.password_reset, name='password_reset'),
    path('password_reset_form/<uidb64>/<token>/', app_views.password_reset_form, name='password_reset_form'),

    # API Urls
    path('download_data/', app_views.download_data, name='download_data'),

    # Map Urls
    path('mapa/', app_views.map, name='map'),

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

    # Room
    path('room/',
        app_views.CustomListView.as_view(
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

    # Container
    path('container/',
        app_views.CustomListView.as_view(
            model=app_models.Container),
        name='container_list'),

    path('container/crear',
        app_views.CustomCreateView.as_view(
            model=app_models.Container),
        name='container_create'),

    path('container/<int:id>/editar',
        app_views.CustomUpdateView.as_view(
            model=app_models.Container),
        name='container_update'),

    path('container/<int:id>/ver',
        app_views.CustomDetailView.as_view(
            model=app_models.Container),
        name='container_view'),

    path('container/<int:id>/borrar',
        app_views.CustomDeleteView.as_view(
            model=app_models.Container),
        name='containerdelete'),

    # Product Urls
    path('product/',
        app_views.CustomListView.as_view(
            model=app_models.Product),
        name='product_list'),

    path('product/crear',
        app_views.CustomCreateView.as_view(
            model=app_models.Product),
        name='product_create'),

    path('product/<int:id>/editar',
        app_views.CustomUpdateView.as_view(
            model=app_models.Product),
        name='product_update'),

    path('product/<int:id>/ver',
        app_views.CustomDetailView.as_view(
            model=app_models.Product),
        name='product_view'),

    path('product/<int:id>/borrar',
        app_views.CustomDeleteView.as_view(
            model=app_models.Product),
        name='product_delete'),

    # Maintenance Tasks Urls
    path('maintenance/',
        app_views.CustomListView.as_view(
            model=app_models.MaintenanceTask),
        name='maintenance_list'),

    path('maintenance/crear',
        app_views.CustomCreateView.as_view(
            model=app_models.MaintenanceTask),
        name='maintenance_create'),

    path('maintenance/<int:id>/editar',
        app_views.CustomUpdateView.as_view(
            model=app_models.MaintenanceTask),
        name='maintenance_update'),

    path('maintenance/<int:id>/ver',
        app_views.CustomDetailView.as_view(
            model=app_models.MaintenanceTask),
        name='maintenance_view'),

    path('maintenance/<int:id>/borrar',
        app_views.CustomDeleteView.as_view(
            model=app_models.MaintenanceTask),
        name='maintenance_delete'),

    # Permissions Urls
    path('permissions/',
        app_views.CustomListView.as_view(
            model=app_models.CustomPermission),
        name='permission_list'),

    # path('permissions/crear', app_views.CustomCreateView.as_view(model=app_models.CustomPermission), name='permission_create'),

    path('permissions/crear/', app_views.permission_create, name='permission_create'),
    path('permissions/crear/cargar_elementos/', app_views.permission_load, name='ajax_permissions_load'),

    path('permissions/<int:id>/editar',
        app_views.CustomUpdateView.as_view(
            model=app_models.CustomPermission),
        name='permission_update'),

    path('permissions/<int:id>/ver',
        app_views.CustomDetailView.as_view(
            model=app_models.CustomPermission),
        name='permission_view'),

    path('permissions/<int:id>/borrar',
        app_views.CustomDeleteView.as_view(
            model=app_models.CustomPermission),
        name='permission_delete'),

    # Statistics Urls
    path('statistics/', app_views.general_statistics, name='general_statistics'),
    #path('room_statistics/<int:id>/', app_views.room_statistics, name='room_statistics'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




#
