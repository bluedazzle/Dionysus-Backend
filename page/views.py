# coding: utf-8
from __future__ import unicode_literals

# Create your views here.
from django.views.generic import DetailView, TemplateView, RedirectView

from core.models import Share


class ShareDetailView(DetailView):
    http_method_names = ['get']
    model = Share
    pk_url_kwarg = 'vid'
    template_name = 'share.html'

    def get_object(self, queryset=None):
        obj = super(ShareDetailView, self).get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

    def get_random(self, visitor):
        return visitor + 1


class GuideView(TemplateView):
    template_name = 'guide.html'


class AppRedirectView(RedirectView):
    url = 'https://itunes.apple.com/cn/app/id1156043950'
    http_method_names = ['get']
