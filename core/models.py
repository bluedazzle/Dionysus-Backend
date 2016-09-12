from __future__ import unicode_literals

from django.db import models


# Create your models here.


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Video(BaseModel):
    cls_choices = [
        (1, 'movie'),
        (2, 'mv'),
        (3, 'funny')
    ]

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128, null=True, blank=True)
    reference = models.CharField(max_length=128, null=True, blank=True)
    thumb_nail = models.CharField(max_length=256, default='')
    url = models.CharField(max_length=128, unique=True)
    classification = models.IntegerField(choices=cls_choices, default=1)
    like = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class AvatarTrack(BaseModel):
    video = models.ForeignKey(Video, related_name='video_tracks')
    data = models.TextField()

    def __unicode__(self):
        return self.video.title


class Secret(BaseModel):
    secret = models.CharField(max_length=64, unique=True)
    remark = models.CharField(max_length=20, default='web')

    def __unicode__(self):
        return self.remark
