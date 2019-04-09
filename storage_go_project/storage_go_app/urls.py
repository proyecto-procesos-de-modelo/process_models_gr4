
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path


from storage_go_app import views as app_views

urlpatterns = [

    #Room Urls

    path('room/',
        app_views.CustomListView.as_view(
            model=app_models.MoveRoom),
        name='room_list'),

    path('room/crear',
        app_views.CustomCreateView.as_view(
            model=app_models.MoveRoom),
        name='room_create'),

    path('room/<int:id>/editar',
        app_views.CustomUpdateView.as_view(
            model=app_models.MoveRoom),
        name='room_update'),

    path('room/<int:id>/ver',
        app_views.CustomDetailView.as_view(
            model=app_models.MoveRoom),
        name='room_view'),

    path('room/<int:id>/borrar',
        app_views.CustomDeleteView.as_view(
            model=app_models.MoveRoom),
        name='room_delete'),


]
