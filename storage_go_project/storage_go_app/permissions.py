
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission

from storage_go_app import models


# Create your permissions here.
def check_permissions(request, user_id=None, permission=None): # pass user
    """
    """

    print("check permissions function")

    user = get_object_or_404(User, pk=request.user.id)
    print(user)

    #groups = user.groups.all()
    #print(groups)

    #permissions = user.user_permissions

    #check group
    user_groups = user.groups.all()
    print(user_groups)

    # show info or not
    if group in user_groups:
        return True
    else:
        return False
