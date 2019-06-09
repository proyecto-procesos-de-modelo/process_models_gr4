
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from storage_go_app import config as storage_config


# Create your utilities here.
def getExcludeFields(model, action):
    """
    """

    fields = None

    if model == 'Salas':
        if action == 'list':
            fields = storage_config.room_list_exclude_fields
        elif action == 'create':
            fields = storage_config.room_create_exclude_fields
        elif action == 'update':
            fields = storage_config.room_update_exclude_fields
        elif action == 'view':
            fields = storage_config.room_view_exclude_fields

    elif model == 'Productos':
        if action == 'list':
            fields = storage_config.product_list_exclude_fields
        elif action == 'create':
            fields = storage_config.product_create_exclude_fields
        elif action == 'update':
            fields = storage_config.product_update_exclude_fields
        elif action == 'view':
            fields = storage_config.product_view_exclude_fields

    elif model == 'Contenedores':
        if action == 'list':
            fields = storage_config.container_list_exclude_fields
        elif action == 'create':
            fields = storage_config.container_create_exclude_fields
        elif action == 'update':
            fields = storage_config.container_update_exclude_fields
        elif action == 'view':
            fields = storage_config.container_view_exclude_fields

    elif model == 'Tareas de Movimiento':
        if action == 'list':
            fields = storage_config.task_list_exclude_fields
        elif action == 'create':
            fields = storage_config.task_create_exclude_fields
        elif action == 'update':
            fields = storage_config.task_update_exclude_fields
        elif action == 'view':
            fields = storage_config.task_view_exclude_fields

    elif model == 'Tareas de Mantenimiento':
        if action == 'list':
            fields = storage_config.maintenance_list_exclude_fields
        elif action == 'create':
            fields = storage_config.maintenance_create_exclude_fields
        elif action == 'update':
            fields = storage_config.maintenance_update_exclude_fields
        elif action == 'view':
            fields = storage_config.maintenance_view_exclude_fields

    elif model == 'Permisos Personalizados':
        if action == 'list':
            fields = storage_config.permission_list_exclude_fields
        elif action == 'create':
            fields = storage_config.permission_create_exclude_fields
        elif action == 'update':
            fields = storage_config.permission_update_exclude_fields
        elif action == 'view':
            fields = storage_config.permission_view_exclude_fields

    elif model == 'Presupuestos':
        if action == 'list':
            fields = storage_config.budget_list_exclude_fields
        elif action == 'create':
            fields = storage_config.budget_create_exclude_fields
        elif action == 'update':
            fields = storage_config.budget_update_exclude_fields
        elif action == 'view':
            fields = storage_config.budget_view_exclude_fields

    elif model == 'Notificaciones':
        if action == 'list':
            fields = storage_config.notification_list_exclude_fields
        elif action == 'create':
            fields = storage_config.notification_create_exclude_fields
        elif action == 'update':
            fields = storage_config.notification_update_exclude_fields
        elif action == 'view':
            fields = storage_config.notification_view_exclude_fields

    return fields


def getProfileRedirectUrl(group):
    """
    """

    url = None

    if group.id == 6:
        url = storage_config.ceo_profile_redirect

    elif group.id == 7:
        url = storage_config.manager_profile_redirect

    elif group.id == 8:
        url = storage_config.maintenance_profile_redirect

    elif group.id == 9:
        url = storage_config.worker_profile_redirect

    elif group.id == 10:
        url = storage_config.admin_profile_redirect

    return url


def getRedirectUrl(name):
    """
    """

    url = None

    if name == 'Salas':
        url = storage_config.room_redirect

    elif name == 'Productos':
        url = storage_config.product_redirect

    elif name == 'Productos':
        url = storage_config.container_redirect

    elif name == 'Tareas de Movimiento':
        url = storage_config.task_redirect

    elif name == 'Tareas de Mantenimiento':
        url = storage_config.maintenance_redirect

    elif name == 'Permisos Personalizados':
        url = storage_config.permission_redirect

    elif name == 'Presupuestos':
        url = storage_config.budget_redirect

    elif name == 'Notificaciones':
        url = storage_config.notification_redirect

    return url


def getUrls(name):

    urls = None

    if name == 'Salas':
        urls = storage_config.room_urls

    elif name == 'Productos':
        urls = storage_config.product_urls

    elif name == 'Contenedores':
        urls = storage_config.container_urls

    elif name == 'Tareas de Movimiento':
        urls = storage_config.task_urls

    elif name == 'Tareas de Mantenimiento':
        urls = storage_config.maintenance_urls

    elif name == 'Permisos Personalizados':
        urls = storage_config.permission_urls

    elif name == 'Presupuestos':
        urls = storage_config.budget_urls

    elif name == 'Notificaciones':
        urls = storage_config.notification_urls

    return urls




#
