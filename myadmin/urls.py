from django.conf.urls import patterns, url
from myadmin.views import *

urlpatterns = patterns('',
                       url(r'video', AdminIndexView.as_view()),
                       url(r'login', AdminView.as_view()),
                       )
