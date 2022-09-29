"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import os
from core.settings import BASE_DIR
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('snippets.urls')),
    
    # path('index/', TemplateView.as_view(template_name='index.html'),
    #                     name='index'),
    # path('index-2/', TemplateView.as_view(template_name='index-2.html'),
    #                     name='index-2'),
]

dir = os.path.join(BASE_DIR, 'templates')
file_list = os.listdir(dir)
for file in file_list:
    path_url = file.replace('.html', '/')
    name = file.replace('.html', '')
    route = path(path_url, TemplateView.as_view(template_name=file),
                        name=name)
    urlpatterns.append(route)
