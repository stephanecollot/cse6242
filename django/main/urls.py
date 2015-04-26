from django.conf.urls import patterns, url

from main import views
from django.conf import settings

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^add/(?P<text>.*)$', views.add, name='add'),
  url(r'^remove/(?P<text>.*)$', views.remove, name='remove'),
  url(r'^chart$', views.chart, name='chart'),
)

urlpatterns += patterns('',
  url(r'^s/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': 'main/templates/s',
  }),)