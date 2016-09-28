from django.conf.urls import patterns, url

from api.views import VideoListView, VideoDetailView, ShareView

urlpatterns = patterns('',
                       url(r'videos', VideoListView.as_view()),
                       url(r'video/(?P<id>(\d)+)', VideoDetailView.as_view()),
                       url(r'share', ShareView.as_view()),
                       )
