from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'key/$', views.KeyDetail.as_view()),
]
