"""justletic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin

from keys import views as keys_views
from keys import urls as keys_urls
from accounts import urls as accounts_urls
from API import urls as API_urls

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^$', keys_views.home_page, name='home'),
    url(r'^users/', include(keys_urls)),
    url(r'^accounts/', include(accounts_urls)),
    url(r'^API/', include(API_urls)),
]
