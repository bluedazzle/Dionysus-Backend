# coding: utf-8
from __future__ import unicode_literals

import json

from django.views.generic import ListView, DetailView

from core.Mixin.CheckMixin import CheckSecurityMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin
from core.models import Video, AvatarTrack


class VideoListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Video
    paginate_by = 10
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = super(VideoListView, self).get_queryset()
        cls = self.request.GET.get('type', 1)
        popular = self.request.GET.get('popular', None)
        if popular:
            queryset = queryset.order_by('like')
        else:
            queryset = queryset.filter(classification=cls)
        return queryset

    def post(self, request, *args, **kwargs):
        cls_choices = {'电影': 1, 'mv': 2, '搞笑': 3}
        json_data = json.loads(request.body)
        cls = json_data.get('classification')
        tracks = json_data.get('tracks')
        if tracks:
            cls = cls_choices[cls]
            title = json_data.get('title')
            author = json_data.get('author')
            reference = json_data.get('reference')
            url = json_data.get('url')
            vs = Video.objects.filter(url=url)
            if not vs.exists():
                thumb_nail = '{0}?vframe/jpg/offset/1/w/200/h/200/'.format(url)
                Video(title=title,
                      url=url,
                      author=author,
                      reference=reference,
                      thumb_nail=thumb_nail,
                      classification=cls).save()
            video = Video.objects.get(url=url)
            AvatarTrack(data=tracks, video=video).save()
            return self.render_to_response({})
        self.message = '追踪数据缺失'
        self.status_code = INFO_NO_EXIST
        return self.render_to_response({})


class VideoDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    pk_url_kwarg = 'id'
    http_method_names = ['get']
    exclude_attr = ['modify_time']

    def get_object(self, queryset=None):
        obj = super(VideoDetailView, self).get_object(queryset)
        track_list = obj.video_tracks.all()
        if track_list.exists():
            setattr(obj, 'tracks', track_list)
        else:
            setattr(obj, 'tracks', [])
        return obj
