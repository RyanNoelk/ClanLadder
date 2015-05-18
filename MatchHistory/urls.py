from django.conf.urls import patterns, url
from MatchHistory import views

urlpatterns = patterns('',
    url(r'^SubmitText/$', views.SubmitText, name='SubmitText'),
    url(r'^SubmitReplay/$', views.SubmitReplay, name='SubmitReplay'),
    url(r'^GetPlayerRaceAndCountry/(?P<player_name>\w+)/$', views.GetPlayerRaceAndCountry, name='GetPlayerRaceAndCountry'),
    url(r'^GetPlayerList/$', views.GetPlayerList, name='GetPlayerList'),
    url(r'^Update/$', views.Update, name='Update'),
    url(r'^FindPlayer/$', views.FindPlayer, name='FindPlayer'),
    url(r'^Player/(?P<player_name>\w+)/$', views.PlayerHistory, name='PlayerHistory'),
    url(r'^', views.index, name='index'),
)