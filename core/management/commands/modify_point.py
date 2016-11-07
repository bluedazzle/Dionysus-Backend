# coding: utf-8

from django.core.management.base import BaseCommand

from core.models import AvatarTrack


class Command(BaseCommand):
    def handle(self, *args, **options):
        id = args[0]
        at = AvatarTrack.objects.filter(id=id)
        if at.exists():
            at = at[0]
            data = eval(at.data)
            for itm in data:
                dw = itm['size']
                dh = dw * 1.33
                dw = dw / 2
                itm['x'] += dw
                itm['y'] += dh
            at.data = unicode(data)
            at.save()

