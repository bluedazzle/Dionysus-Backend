# coding: utf-8

from django.core.management.base import BaseCommand

from core.models import Share, Video


class Command(BaseCommand):
    def handle(self, *args, **options):
        for itm in Share.objects.all():
            if not itm.source:
                itm.source = Video.objects.get(url='del')
                itm.save()
