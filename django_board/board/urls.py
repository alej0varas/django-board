from django.conf.urls import patterns, include, url

from .views import MainBoardPage


urlpatterns = patterns(
    '',
    url(r'^$', MainBoardPage.as_view(), name='main'),
)
