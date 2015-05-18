from django.conf.urls import patterns, url
from Ladder import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^HowITWorks/$', views.HowITWorks, name='HowITWorks'),
    url(r'^Contact/$', views.Contact, name='Contact'),
)