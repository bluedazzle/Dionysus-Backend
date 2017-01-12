# coding: utf-8

from __future__ import unicode_literals
from django.contrib.sitemaps import Sitemap

from core.models import Share


class ShareSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Share.objects.all()

    def lastmod(self, item):
        return item.create_time

    def location(self, item):
        return r'/page/share/{0}'.format(item.id)
