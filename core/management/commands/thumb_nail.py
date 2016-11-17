from django.core.management.base import BaseCommand

from core.models import Video


class Command(BaseCommand):
    def handle(self, *args, **options):
        for itm in Video.objects.all():
            itm.thumb_nail = itm.thumb_nail.replace("/1/", "/0/")
            itm.save()
