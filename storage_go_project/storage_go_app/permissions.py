
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q

from storage_go_app import models as storage_models


# Create your permissions here.
def check_permissions(username=None, type=None, action=None, model=None, object=None, attribute=None):
    """
    """

    #print("check permissions function")

    #print(type)
    #print(action)
    #print(model)
    #print(object)
    #print(attribute)

    user = get_object_or_404(User, username=username)
    groups = user.groups.all()

    permissions = storage_models.CustomPermission.objects.filter(
        group__in=groups,
    )

    if type == 'Modelo':
        permissions = permissions.filter(
            type=type,
            action=action,
            model=model
        )

    elif type == 'Objeto':
        permissions = permissions.filter(
            Q(type=type) &
            Q(action=action) &
            Q(model=model) &
            (Q(object=object) |
            Q(object='Todos'))
        )

    elif type == 'Atributo':
        permissions = permissions.filter(
            Q(type=type) &
            Q(action=action) &
            Q(model=model) &
            (Q(object=object) |
            Q(object='Todos')) &
            Q(attribute=attribute) |
            Q(attribute='Todos')
    )
    #print(permissions)

    # show info or not
    if permissions:
        return True
    else:
        return False
