
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import template

from django.shortcuts import get_object_or_404

from storage_go_app import models as storage_models


register = template.Library()


# Create your tags here
@register.simple_tag
def get_url(dictionary, key):
    """
    """

    return dictionary.get(key)


@register.simple_tag
def get_room(room_id):
    """
    """

    room = get_object_or_404(storage_models.Room, id=str(room_id))

    return room


@register.simple_tag
def setValue(value):
    """
    """

    return value




#
