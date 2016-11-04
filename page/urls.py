from django.conf.urls import patterns, include, url
from page.views import *

from Dionysus import settings

urlpatterns = patterns('',
                       url(r'^share/(?P<vid>(\d)+)', ShareDetailView.as_view()),
                       url(r'^guide', GuideView.as_view()),
                       )
