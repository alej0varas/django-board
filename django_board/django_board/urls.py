from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^board/', include('board.urls', namespace='board')),
)
