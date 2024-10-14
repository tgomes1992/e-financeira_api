"""portalescrituracao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [ path("", list_bucket_files, name="sqarquivos"),
                path('download', download_unique ,  name='download_by_key') ,
                path('delete_file' ,  delete_by_key, name='delete_by_key')  ,
                path('dowload_prefix_as_zip', dowload_prefix_as_zip, name='download_by_zip'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
