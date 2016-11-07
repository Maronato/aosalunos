from django.conf.urls import url
from app import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='home_index'),
    url(r'^sobre/$', views.about, name='home_about'),
    url(r'^propostas/$', views.promises, name='home_promises'),
    url(r'^consu/$', views.consu, name='home_consu'),
    url(r'^participe/$', views.join, name='home_join'),
    url(r'^logout/$', views.logout, name='home_logout'),

    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='app/robots.txt', content_type='text/plain')),
    url(r'^humans\.txt$', TemplateView.as_view(
        template_name='app/humans.txt', content_type='text/plain')),

]
