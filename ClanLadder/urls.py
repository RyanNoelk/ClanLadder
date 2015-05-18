from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('',
    url('', include('Ladder.urls', namespace='Ladder')),
    url(r'^Matches/', include('MatchHistory.urls', namespace='MatchHistory')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^Accounts/', include('Accounts.urls', namespace='Accounts')),
)