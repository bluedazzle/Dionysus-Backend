# coding: utf-8

from django.core.management.base import BaseCommand

from core.models import Video


class Command(BaseCommand):
    def handle(self, *args, **options):
        for itm in Video.objects.all():
            itm.url = itm.url.replace('oda176fz0.bkt.clouddn.com', 'static.fibar.cn')
            itm.save()
