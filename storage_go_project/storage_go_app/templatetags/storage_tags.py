
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import template

from django.shortcuts import get_object_or_404

from storage_go_app import models as storage_models
from storage_go_app import permissions as storage_permissions

register = template.Library()


# Create your tags here
@register.simple_tag
def get_url(dictionary, key):
    """
    """

    return dictionary.get(key)


@register.simple_tag
def get_room(room_name):
    """
    """
    room = get_object_or_404(storage_models.Room, name=room_name)

    return room


@register.simple_tag
def get_container(room_map_id):
    """
    """
    try:
        container = get_object_or_404(storage_models.Container, room_map=room_map_id)
        return container
    except:
        return ''


@register.simple_tag
def setValue(value):
    """
    """

    return value


@register.simple_tag
def getNotifications(user_id):
    """
    """

    notifications = storage_models.Notification.objects.filter(user_id=user_id)

    return notifications


@register.simple_tag
def check_permission(username, type=None, action=None, model=None, object=None, attribute=None):
    """
    """

    if storage_permissions.check_permissions(username, type, action, model, object, attribute):
        return True
    else:
        return False



#
