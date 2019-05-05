
#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from django.contrib import admin

from storage_go_app import models

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('id', 'status', 'name', 'humidity', 'temperature', 'max_containers')
    list_filter = ('status', )
    search_fields = ('name', )
    list_editable = ('status', 'name')

admin.site.register(models.Room, RoomAdmin)

class RoomMapAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('id', 'status', 'room', 'x', 'y')
    list_filter = ('status', 'room')
    #search_fields = ('name', )
    list_editable = ('status', 'room', 'x', 'y')

admin.site.register(models.RoomMap, RoomMapAdmin)

admin.site.register(models.Product)

admin.site.register(models.Container)

admin.site.register(models.MoveTask)

admin.site.register(models.MaintenanceTask)

admin.site.register(models.CustomPermission)




#
