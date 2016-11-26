from django.conf.urls import patterns, url

from api.views import VideoListView, VideoDetailView, ShareView, UploadView, ShareDetailView, ShareListView, NotifyView, \
    VideoModifyView, VideoDetailHiddenView, VideoOrderView

urlpatterns = patterns('',
                       url(r'videos', VideoListView.as_view()),
                       url(r'video/(?P<id>(\d)+)/like', VideoModifyView.as_view()),
                       url(r'video/(?P<id>(\d)+)/order', VideoOrderView.as_view()),
                       url(r'video/(?P<id>(\d)+)/hidden', VideoDetailHiddenView.as_view()),
                       url(r'video/(?P<id>(\d)+)', VideoDetailView.as_view()),
                       url(r'shares', ShareListView.as_view()),
                       url(r'share/(?P<id>(\d)+)', ShareDetailView.as_view()),
                       url(r'share', ShareView.as_view()),
                       url(r'upload', UploadView.as_view()),
                       url(r'notify', NotifyView.as_view()),
                       )
