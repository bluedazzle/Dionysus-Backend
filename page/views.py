# coding: utf-8
from __future__ import unicode_literals

# Create your views here.
from django.views.generic import DetailView, TemplateView, RedirectView, ListView

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


class AppRedirectView(ListView):
    template_name = 'index.html'
    model = Share
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super(AppRedirectView, self).get_queryset()
        return queryset[:10]
