from django.conf.urls import url
from aptechapi import views

#username: aptech, password: apt3ch123
#email : aptechconnectug@gmail.com, password: T9w3y5

urlpatterns = [
    url(r'^login/$', views.api_login, name='apcon_api_login'),
    url(r'^articles/all/(?P<token>[^/]+)/$', views.api_get_articles, name='apcon_api_articles'),
    url(r'^articles/new/(?P<token>[^/]+)/$', views.api_post_article, name='apcon_api_post_article'),
    url(r'^articles/comment/add/(?P<token>[^/]+)/$', views.api_post_comment, name='apcon_api_add_comment'),
    url(r'^events/all/(?P<token>[^/]+)/$', views.api_get_events, name='apcon_api_articles'),
    url(r'^users/all/(?P<token>[^/]+)/$', views.api_get_users, name='apcon_api_users'),
    url(r'^books/all/(?P<token>[^/]+)/$', views.api_get_books, name='apcon_api_books'),
    url(r'^users/edit/image/add/(?P<token>[^/]+)/$', views.api_update_user_image, name='apcon_api_edit_image'),
    url(r'^feedback/send/(?P<token>[^/]+)/$', views.api_post_feed_back, name='apcon_api_send_feedback'),
    url(r'^messages/load/(?P<token>[^/]+)/user/(?P<user_id>\d+)/$', views.api_get_messages, name='apcon_api_messages'),
    url(r'^messages/send/(?P<token>[^/]+)/user/(?P<user_id>\d+)/$', views.api_send_message, name='apcon_api_send_message'),

]