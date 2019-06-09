
#!/usr/local/bin/python
# -*- coding: utf-8 -*-


# urls for each model
room_urls = {
    'list': 'panel:room_list',
    'create': 'panel:room_create',
    'view': 'panel:room_view',
    'delete': 'panel:room_delete',
    'update': 'panel:room_update',
}

product_urls = {
    'list': 'panel:product_list',
    'create': 'panel:product_create',
    'view': 'panel:product_view',
    'delete': 'panel:product_delete',
    'update': 'panel:product_update',
}

container_urls = {
    'list': 'panel:container_list',
    'create': 'panel:container_create',
    'view': 'panel:container_view',
    'delete': 'panel:container_delete',
    'update': 'panel:container_update',
}

task_urls = {
    'list': 'panel:task_list',
    'create': 'panel:task_create',
    'view': 'panel:task_view',
    'delete': 'panel:task_delete',
    'update': 'panel:task_update',
}

maintenance_urls = {
    'list': 'panel:maintenance_list',
    'create': 'panel:maintenance_create',
    'view': 'panel:maintenance_view',
    'delete': 'panel:maintenance_delete',
    'update': 'panel:maintenance_update',
}

permission_urls = {
    'list': 'panel:permission_list',
    'create': 'panel:permission_create',
    'view': 'panel:permission_view',
    'delete': 'panel:permission_delete',
    'update': 'panel:permission_update',
}

budget_urls = {
    'list': 'panel:budget_list',
    'create': 'panel:budget_create',
    'view': 'panel:budget_view',
    'delete': 'panel:budget_delete',
    'update': 'panel:budget_update',
}

notification_urls = {
    'list': 'panel:notification_list',
    'create': 'panel:notification_create',
    'view': 'panel:notification_view',
    'delete': 'panel:notification_delete',
    'update': 'panel:notification_update',
}


# exclude attributes for each model
room_create_exclude_fields = []
room_list_exclude_fields = ['room_map', 'maintenance_task_room']
room_update_exclude_fields = ['room_map', 'maintenance_task_room']
room_view_exclude_fields = ['maintenance_task_room']

product_create_exclude_fields = ['container_product', 'entry_date']
product_list_exclude_fields = ['container_product']
product_update_exclude_fields = ['container_product', 'entry_date']
product_view_exclude_fields = ['container_product']

container_create_exclude_fields = []
container_list_exclude_fields = []
container_update_exclude_fields = []
container_view_exclude_fields = []

task_create_exclude_fields = []
task_list_exclude_fields = []
task_update_exclude_fields = []
task_view_exclude_fields = []

maintenance_create_exclude_fields = ['budget_task']
maintenance_list_exclude_fields = ['budget_task']
maintenance_update_exclude_fields = ['budget_task']
maintenance_view_exclude_fields = ['budget_task']

permission_create_exclude_fields = []
permission_list_exclude_fields = []
permission_update_exclude_fields = []
permission_view_exclude_fields = []

budget_create_exclude_fields = []
budget_list_exclude_fields = []
budget_update_exclude_fields = []
budget_view_exclude_fields = []

notification_create_exclude_fields = []
notification_list_exclude_fields = []
notification_update_exclude_fields = []
notification_view_exclude_fields = ['user', 'model', 'object', 'content_object']


# field types
related_fields = ['ManyToManyField', 'ManyToOneRel']

# redirect urls
room_redirect = 'panel:map'
product_redirect = 'panel:product_list'
container_redirect = 'panel:container_list'
task_redirect = 'panel:task_list'
maintenance_redirect = 'panel:maintenance_list'
permission_redirect = 'panel:permission_list'
budget_redirect = 'panel:budget_list'
notification_redirect = 'panel:map'

# redirect base on profile
maintenance_profile_redirect = 'panel:maintenance_list'
worker_profile_redirect = 'panel:task_list'
ceo_profile_redirect = 'panel:general_statistics'
manager_profile_redirect = 'panel:task_list'
admin_profile_redirect = 'admin/'



#
