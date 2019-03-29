from django.conf.urls import url
from aptechapi import views

#username: aptech, password: apt3ch123

urlpatterns = [
    url(r'^login/$', views.api_login, name='apcon_api_login'),
    url(r'^articles/all/(?P<token>[^/]+)/$', views.api_get_articles, name='apcon_api_articles'),
    url(r'^articles/new/(?P<token>[^/]+)/$', views.api_post_article, name='apcon_api_post_article'),
    url(r'^articles/comment/add/(?P<token>[^/]+)/$', views.api_post_comment, name='apcon_api_add_comment'),
    url(r'^events/all/(?P<token>[^/]+)/$', views.api_get_events, name='apcon_api_articles'),
]