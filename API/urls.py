from django.conf.urls import url

from rest_framework.authtoken import views as rest_framework_views

from . import views

urlpatterns = [
    url(r'^key/$', views.KeyDetail.as_view(), name='key_detail'),
    url(r'^user/$', views.UserList.as_view(), name='user_list'),
    url(r'^token/$', views.TokenList.as_view(), name='token_list'),
#    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'), 
]
