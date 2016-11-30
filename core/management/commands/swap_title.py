# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

from core.models import Video


class Command(BaseCommand):
    def handle(self, *args, **options):
        for itm in Video.objects.all():
            itm.wechat_title = ''
            itm.wechat_sub_title = '变身热门短视频中的主角，释放你的洪荒之力，快来一起玩吧~'
            itm.save()
