from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from Accounts import views


urlpatterns = patterns('',
    url(r'^Logout/$', views.Logout, name='Logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'Accounts/login.html'}, name='login'),
    url(r'^password/change/$', views.PasswordChange, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, {'template_name': 'Accounts/password_change_done.html'}, name='password_change_done'),
    
)