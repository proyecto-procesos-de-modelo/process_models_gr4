
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Storage & Go'
admin.autodiscover()

from storage_go_app import urls as app_urls
from storage_go_app import views as app_views

urlpatterns = [
  
    # App Urls
    path('', include(app_urls, 'app'), namespace='app'),

    # Admin Urls
    path('admin/', admin.site.urls),
]
