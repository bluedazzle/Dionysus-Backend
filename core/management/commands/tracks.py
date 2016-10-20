from django.core.management.base import BaseCommand

from core.models import Video, AvatarTrack
from core.tracks import format_tracks_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        vid = args[0]
        video = Video.objects.filter(id=vid)
        if video.exists():
            video = video[0]
            tracks_data = AvatarTrack.objects.filter(video=video)
            if tracks_data.exists():
                tracks_data = tracks_data[0]
                data = unicode(format_tracks_data(tracks_data.data, video.total_frames, video.duration))
                tracks_data.data = data
                tracks_data.save()
