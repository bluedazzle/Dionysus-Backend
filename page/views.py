# coding: utf-8
from __future__ import unicode_literals

# Create your views here.
from django.views.generic import DetailView

from core.models import Share


class ShareDetailView(DetailView):
    http_method_names = ['get']
    model = Share
    pk_url_kwarg = 'vid'
    template_name = 'share.html'
