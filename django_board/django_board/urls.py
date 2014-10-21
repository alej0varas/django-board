from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^board/', include('board.urls', namespace='board')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
