from django.conf.urls import url
from aptechapi import views

#username: aptech, password: apt3ch123

urlpatterns = [
    url(r'^login/$', views.api_login, name='apcon_api_login'),
    url(r'^users/all/$', views.api_get_users, name='apcon_api_users')
]