# coding: utf-8

from django.core.management.base import BaseCommand

from core.models import Video, AvatarTrack


class Command(BaseCommand):
    def handle(self, *args, **options):
        for itm in Video.objects.all():
            time = itm.duration
            track = AvatarTrack.objects.get(video=itm)
            data = eval(track.data)
            if data[-1]['time'] != time:
                data[-1]['time'] = time
            track.data = unicode(data)
            track.save()
