# coding: utf-8
from __future__ import unicode_literals
from django.views.generic import ListView, DetailView

from core.Mixin.CheckMixin import CheckSecurityMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin
from core.dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin
from core.models import Video, AvatarTrackc


class VideoListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Video
    paginate_by = 10
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super(VideoListView, self).get_queryset()
        cls = self.request.get('type')
        popular = self.request.get('popular', None)
        if popular:
            queryset = queryset.order_by('like')
        else:
            queryset = queryset.filter(classification=cls)
        return queryset


class VideoView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    pk_url_kwarg = 'id'
    http_method_names = ['get']
