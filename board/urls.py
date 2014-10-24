from django.conf.urls import patterns, include, url

from .views import MainBoardPage, ThreadView


urlpatterns = patterns(
    '',
    url(r'^$', MainBoardPage.as_view(), name='main'),
    url(r'(?P<pk>\d+)/$', ThreadView.as_view(), name='thread')
)
