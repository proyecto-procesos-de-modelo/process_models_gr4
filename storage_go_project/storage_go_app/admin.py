
#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from storage_go_app import models as storage_models

# Register your admin models here.
class RoomAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('id', 'status', 'name', 'humidity', 'temperature', 'max_containers')
    list_filter = ('status', )
    search_fields = ('name', )
    list_editable = ('status', 'name', 'humidity', 'temperature', 'max_containers')

admin.site.register(storage_models.Room, RoomAdmin)


class RoomMapAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('id', 'status', 'room', 'x', 'y')
    list_filter = ('status', 'room')
    #search_fields = ('name', )
    list_editable = ('status', 'room', 'x', 'y')

admin.site.register(storage_models.RoomMap, RoomMapAdmin)

admin.site.register(storage_models.Product)

admin.site.register(storage_models.Container)

admin.site.register(storage_models.Notification)

admin.site.register(storage_models.ActiveUser)

admin.site.register(storage_models.Statistic)

class MoveTaskAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('id', 'status', 'worker', 'priority', 'container', 'destination')
    list_filter = ('status', 'worker', 'priority')
    #search_fields = ('name', )
    list_editable = ('status', 'worker', 'priority', 'container', 'destination')

admin.site.register(storage_models.MoveTask, MoveTaskAdmin)

admin.site.register(ContentType)

admin.site.register(storage_models.MaintenanceTask)

admin.site.register(storage_models.Budget)

class CustomPermissionAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('id', 'group', 'type', 'action', 'model', 'object', 'attribute')
    list_filter = ('group', 'type', 'action', 'model', 'object', 'attribute' )
    list_editable = ('group', 'type', 'action', 'model', 'object', 'attribute')

admin.site.register(storage_models.CustomPermission, CustomPermissionAdmin)




#
