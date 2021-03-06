"""administrador_encuestas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from adminplus.sites import AdminSitePlus
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from encuestas.views import survey_menu, graph_viewer

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    # ...
    # Include the admin URL conf as normal.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/graphs', graph_viewer),
    url(r'^encuestas/',include('encuestas.urls', namespace='encuestas')),
    url(r'^encuestas/v2/',include('encuestas.apiv2.urls', namespace='encuestasapiv2')),
    # ...
]
urlpatterns += staticfiles_urlpatterns()