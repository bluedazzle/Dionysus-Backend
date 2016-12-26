# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

from core.models import Video


class Command(BaseCommand):
    def handle(self, *args, **options):
        remove_str = args[0]
        for itm in Video.objects.all():
            itm.title.replace(remove_str, '')
            itm.save()
