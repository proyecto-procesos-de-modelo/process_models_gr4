
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = 'Storage & Go'
admin.autodiscover()

from storage_go_app import urls as app_urls
from storage_go_app import views as app_views

urlpatterns = [

    # Redirect
    path('', RedirectView.as_view(url='/panel/mapa/')),

    # App Urls
    path('panel/', include((app_urls, 'panel'), namespace='panel')),

    # Admin Urls
    path('admin/', admin.site.urls),

]
