from django.conf.urls import patterns, url
from views import VistaPaso1, VistaPaso2

urlpatterns = patterns('',
                       url(r'^$', VistaPaso1.as_view(), name="deteccion"),
                       url(r'^resultado/(?P<id_deteccion>\d+)$', VistaPaso2.as_view(), name="resultado"),
                       )