from django.conf.urls import url
from aptechadmin import views

#username: aptech, password: apt3ch123

urlpatterns = [
	url(r'^$', views.dashboard, name='apcon_admin_index'),
    url(r'^login/$', views.AdminLogin.as_view(), name='apcon_admin_login'),
    url(r'^logout/$', views.admin_logout, name='apcon_admin_logout'),
    url(r'^students/$', views.students, name='apcon_admin_students'),
    url(r'students/add/new/$', views.add_new_student, name='apcon_admin_student_add'),
    url(r'articles/$', views.articles, name='apcon_admin_articles'),
    url(r'articles/add/new/$', views.add_new_article, name='apcon_admin_article_add'),
    url(r'events/$', views.events, name='apcon_admin_events'),
    url(r'events/add/new/$', views.add_new_event, name='apcon_admin_event_add'),
    url(r'ebooks/$', views.ebooks, name='apcon_admin_ebooks'),
    url(r'ebooks/add/new/$', views.add_new_book, name='apcon_admin_book_add'),
]