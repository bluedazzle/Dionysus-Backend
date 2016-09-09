from django.conf.urls import patterns, include, url

from api.views import VideoListView

urlpatterns = patterns('',
                       url(r'videos', VideoListView.as_view()),
                       )
