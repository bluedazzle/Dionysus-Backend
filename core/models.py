# coding: utf-8
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
        (3, 'funny'),
        (4, 'variety'),
        (5, 'spring'),
    ]

    default_title = '变身热门短视频中的主角，释放你的洪荒之力，快来一起玩吧~'

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128, null=True, blank=True)
    reference = models.CharField(max_length=128, null=True, blank=True)
    thumb_nail = models.CharField(max_length=256, default='')
    url = models.CharField(max_length=128, unique=True)
    classification = models.IntegerField(choices=cls_choices, default=1)
    like = models.IntegerField(default=0)
    duration = models.FloatField(default=0.0)
    fps = models.IntegerField(default=25)
    total_frames = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    tag = models.CharField(max_length=10, default='', null=True, blank=True)
    has_subtitle = models.BooleanField(default=False)

    weibo_title = models.TextField(default=default_title)
    wechat_title = models.TextField(default='', null=True, blank=True)
    wechat_sub_title = models.TextField(default=default_title)

    def __unicode__(self):
        return self.title


class AvatarTrack(BaseModel):
    video = models.ForeignKey(Video, related_name='video_tracks')
    data = models.TextField()
    subtitle = models.TextField(null=True, blank=True)
    has_sub = models.BooleanField(default=False)

    def __unicode__(self):
        return self.video.title


class Secret(BaseModel):
    secret = models.CharField(max_length=64, unique=True)
    remark = models.CharField(max_length=20, default='web')

    def __unicode__(self):
        return self.remark


class MyUser(models.Model):
    uid = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.uid


class Share(BaseModel):
    pid = models.CharField(max_length=256, default='', blank=True, null=True)
    source = models.ForeignKey(Video, related_name='video_shares', null=True, blank=True)
    url = models.CharField(max_length=256)
    thumb_nail = models.CharField(max_length=256, default='')
    author = models.ForeignKey(MyUser, related_name='my_shares')
    token = models.CharField(max_length=64, default='')
    visitor = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    recommend = models.BooleanField(default=False)

    def __unicode__(self):
        return self.author.uid


class Record(BaseModel):
    sign = models.CharField(unique=True, max_length=20)
    ios_count = models.IntegerField(default=0)
    android_count = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.sign


class Banner(BaseModel):
    picture = models.CharField(max_length=256)
    nav = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    remark = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.remark


class Classification(BaseModel):
    name = models.CharField(max_length=10)
    type = models.IntegerField(unique=True)
    icon = models.CharField(max_length=128)
    select_icon = models.CharField(max_length=128)
    index = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name


class Update(BaseModel):
    android_verison = models.CharField(max_length=10)
    android_download = models.CharField(max_length=128)
    android_title = models.CharField(max_length=128)
    android_log = models.TextField()

    def __unicode__(self):
        return self.android_verison
