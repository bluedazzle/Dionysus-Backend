# coding: utf-8
from __future__ import unicode_literals

import json
import random

import requests
import time
import xlwt as xlwt

from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, DeleteView, View, UpdateView

from core.Mixin.CheckMixin import CheckSecurityMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin
from core.models import Video, AvatarTrack, Share, MyUser, Record, Banner, Classification, Update
from core.qn import delete_file, generate_upload_token, add_water_mask
from core.tracks import format_tracks_data
from core.utils import serialize_srt
from core.wechat_sign import wechat_sign


class VideoListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Video
    paginate_by = 20
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = super(VideoListView, self).get_queryset().order_by("-hidden", "-has_subtitle", "-create_time")
        cls = self.request.GET.get('type', 1)
        all = self.request.GET.get('all', None)
        search = self.request.GET.get('search', None)
        dev = self.request.GET.get('dev', None)
        if not dev:
            queryset = queryset.filter(hidden=False).order_by("-create_time")
        if search and search != '':
            queryset = queryset.filter(Q(title__icontains=search) |
                                       Q(reference__icontains=search) |
                                       Q(author__icontains=search))
        popular = self.request.GET.get('like', None)
        if popular:
            queryset = queryset.order_by("-like", "-create_time")
        else:
            if not all:
                queryset = queryset.filter(classification=cls)
            if not search and not dev:
                queryset = queryset.order_by('-order', '-create_time')
        return queryset

    def post(self, request, *args, **kwargs):
        cls_choices = {'电影': 1, 'mv': 2, '搞笑': 3, '综艺': 4, '春节': 5}
        json_data = json.loads(request.body)
        cls = json_data.get('classification')
        total_frames = int(json_data.get('frames', 0))
        duration = float(json_data.get('duration', 0.0))
        fps = int(json_data.get('fps', 25))
        tracks = json_data.get('tracks')
        if tracks:
            cls = cls_choices.get(cls, 1)
            title = json_data.get('title')
            author = json_data.get('author')
            reference = json_data.get('reference')
            url = json_data.get('url')
            url = url.replace('oda176fz0.bkt.clouddn.com', 'static.fibar.cn')
            vs = Video.objects.filter(url=url)
            if not vs.exists():
                thumb_nail = '{0}?vframe/jpg/offset/0/w/200/h/200/'.format(url)
                Video(title=title,
                      url=url,
                      author=author,
                      reference=reference,
                      thumb_nail=thumb_nail,
                      total_frames=total_frames,
                      duration=duration,
                      hidden=True,
                      fps=fps,
                      classification=cls).save()
            else:
                vs = vs[0]
                vs.title = title
                vs.author = author
                vs.reference = reference
                vs.save()
            video = Video.objects.get(url=url)
            at = AvatarTrack.objects.filter(video=video)
            if at.exists():
                for itm in at:
                    itm.delete()
            tracks = unicode(format_tracks_data(tracks, total_frames, duration))
            AvatarTrack(data=tracks, video=video).save()
            return self.render_to_response({})
        self.message = '追踪数据缺失'
        self.status_code = INFO_NO_EXIST
        return self.render_to_response({})


class VideoDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DeleteView):
    model = Video
    success_url = ''
    pk_url_kwarg = 'id'
    http_method_names = ['get', 'delete']
    exclude_attr = ['modify_time']

    def get_object(self, queryset=None):
        obj = super(VideoDetailView, self).get_object(queryset)
        track_list = obj.video_tracks.all()
        if track_list.exists():
            track = track_list[0]
            setattr(obj, 'tracks', eval(track.data))
            setattr(obj, 'has_subtitle', track.has_sub)
            if track.has_sub:
                setattr(obj, 'subtitle', eval(track.subtitle))
        else:
            setattr(obj, 'tracks', [])
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        key = unicode(self.object.url).split('/')[-1]
        delete_file(key)
        self.object.delete()
        return self.render_to_response({})


class VideoDetailHiddenView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    pk_url_kwarg = 'id'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            obj.hidden = not obj.hidden
            obj.save()
        return self.render_to_response({})


class VideoModifyView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    pk_url_kwarg = 'id'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        vid = kwargs.get('id')
        video = Video.objects.filter(id=vid)
        if video.exists():
            like = request.POST.get('like')
            if like:
                video = video[0]
                video.like = like
                video.save()
                return self.render_to_response({})
            self.message = '数据缺失'
            self.status_code = ERROR_DATA
            return self.render_to_response({})
        self.message = '视频不存在'
        self.status_code = INFO_NO_EXIST
        return self.render_to_response({})


class VideoSubTitleView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    pk_url_kwarg = 'id'
    http_method_names = ['post']

    def get_object(self, queryset=None):
        obj = super(VideoSubTitleView, self).get_object(queryset)
        at = AvatarTrack.objects.get(video=obj)
        return at, obj

    def post(self, request, *args, **kwargs):
        srt = request.FILES.get('srt', None)
        if not srt:
            self.message = '参数缺失'
            self.status_code = ERROR_DATA
            # return HttpResponseRedirect('/admin/video')
            return self.render_to_response({})
        # try:
        subtitles = serialize_srt(srt.file.readlines())
        at, obj = self.get_object()
        at.subtitle = str(subtitles)
        at.has_sub = True
        at.save()
        obj.has_subtitle = True
        obj.save()
        return HttpResponseRedirect('/admin/video')
        # except Exception, e:
        #     print e
        #     # self.message = '未知错误'
        #     # self.status_code = ERROR_UNKNOWN
        #     # return HttpResponseRedirect('/admin/video')
        #     return self.render_to_response({'error': e})


class VideoOrderView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    pk_url_kwarg = 'id'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        vid = kwargs.get('id')
        video = Video.objects.filter(id=vid)
        if video.exists():
            order = request.POST.get('order')
            if order:
                video = video[0]
                video.order = order
                video.save()
                return self.render_to_response({})
            self.message = '数据缺失'
            self.status_code = ERROR_DATA
            return self.render_to_response({})
        self.message = '视频不存在'
        self.status_code = INFO_NO_EXIST
        return self.render_to_response({})


class ShareView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Share
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        url = request.POST.get('url')
        if 'http://' not in url:
            url = 'http://{0}'.format(url)
        uid = request.POST.get('uid')
        vid = request.POST.get('vid')
        token = request.POST.get('token')

        if url and uid and vid:
            user, created = MyUser.objects.get_or_create(uid=uid)
            video = Video.objects.get(id=vid)
            video.like += 1
            video.save()
            share = Share.objects.filter(token=token, author=user)
            if share.exists():
                share = share[0]
                self.message = '视频已存在'
                share_url = 'http://www.datoushow.com/page/share/{0}'.format(share.id)
                return self.render_to_response({"url": share_url,
                                                "thumb_nail": share.thumb_nail,
                                                'weibo_title': share.source.weibo_title,
                                                'wechat_title': share.source.wechat_title,
                                                'wechat_sub_title': share.source.wechat_sub_title})
            # key = url.split("/")[-1]
            # pid = add_water_mask(key)
            # if not pid:
            #     self.message = '视频不存在或出现错误'
            #     self.status_code = ERROR_DATA
            #     return self.render_to_response({})
            thumb_nail = '{0}?vframe/jpg/offset/1/w/200/h/200/'.format(url)
            Share(url=url, author=user, source=video, thumb_nail=thumb_nail, token=token).save()
            share = Share.objects.get(url=url, author=user)
            share_url = 'http://www.datoushow.com/page/share/{0}'.format(share.id)
            return self.render_to_response({'url': share_url,
                                            "thumb_nail": share.thumb_nail,
                                            'weibo_title': share.source.weibo_title,
                                            'wechat_title': share.source.wechat_title,
                                            'wechat_sub_title': share.source.wechat_sub_title})
        self.message = '参数缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response({})


class RecordView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Record
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        channel = int(request.GET.get('channel', 1))
        obj, status = Record.objects.get_or_create(sign='record')
        if channel == 1:
            obj.ios_count += 1
        else:
            obj.android_count += 1
        obj.save()
        return self.render_to_response({})


class ShareListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Share
    paginate_by = 20
    http_method_names = ['get']
    foreign = True

    # ordering = ('-create_time')

    def get_queryset(self):
        queryset = super(ShareListView, self).get_queryset()
        queryset = queryset.order_by('-recommend', '-create_time')
        return queryset


class ShareDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DeleteView):
    model = Share
    http_method_names = ['get', 'delete']
    pk_url_kwarg = 'id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        key = unicode(self.object.url).split('/')[-1]
        delete_file(key)
        self.object.delete()
        return self.render_to_response({})


class ShareRecommendView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Share
    http_method_names = ['get']
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(ShareRecommendView, self).get_object(queryset)
        obj.recommend = not obj.recommend
        obj.save()
        return self.render_to_response({})


class UploadView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        token = generate_upload_token()
        return self.render_to_response({"token": token})


class NotifyView(UpdateView):
    http_method_names = ['get', 'post']
    model = Share

    def get(self, request, *args, **kwargs):
        print request.body
        return HttpResponse('success')

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        pid = json_data.get('id')
        state = json_data.get('code')
        if state == 0:
            old_key = json_data.get('inputKey')
            new_key = json_data.get('items')[0].get('key')
            share = Share.objects.get(pid=pid)
            url = 'http://static.fibar.cn/{0}'.format(new_key)
            thumb = '{0}?vframe/jpg/offset/1/w/200/h/200/'.format(url)
            share.url = url
            share.thumb_nail = thumb
            share.save()
            delete_file(old_key)
        return HttpResponse('success')


class ClickView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Record

    def get_object(self, queryset=None):
        obj = Record.objects.all()[0]
        obj.click_count += 1
        obj.save()


class BannerListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Banner

    def get_queryset(self):
        queryset = super(BannerListView, self).get_queryset()
        queryset = queryset.filter(active=True)
        return queryset


class ClassificationListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Classification
    exclude_attr = ['create_time', 'modify_time', 'id']
    ordering = 'index'


class UpdateView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Update

    def get_object(self, queryset=None):
        obj = Update.objects.all()[0]
        return obj


class WechatTokenView(StatusWrapMixin, JsonResponseMixin, DetailView):
    def get(self, request, *args, **kwargs):
        token = cache.get('access_token')
        if not token:
            result = requests.get(
                'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx8f04e633e9b5d33c&secret=f5f8353ac90c783fdf71a05f9ee0c835')
            token = json.loads(result.content).get('access_token')
            cache.set("access_token", token, 7200)
        ticket = cache.get('ticket')
        if not ticket:
            result = requests.get(
                'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi'.format(token))
            ticket = json.loads(result.content).get('ticket')
            cache.set('ticket', ticket, 7200)
        res = wechat_sign.sign(request.GET.get('url'), ticket)
        return self.render_to_response(res)


class OutPutView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        queryset = Video.objects.all()
        wb = xlwt.Workbook(encoding='utf-8')
        now_time = time.clock()
        ws = wb.add_sheet(str(now_time))
        ws.write(0, 0, "id")
        ws.write(0, 1, "标题")
        ws.write(0, 2, "作者")
        ws.write(0, 3, "分类")
        ws.write(0, 4, "等级")
        i = 1
        for itm in queryset:
            ws.write(i, 0, itm.id)
            ws.write(i, 1, itm.title)
            ws.write(i, 2, itm.author)
            ws.write(i, 3, itm.cls_choices[itm.classification - 1][1])
            i += 1
        wb.save("static/file/output.xls")
        return HttpResponseRedirect("/static/file/output.xls")

    def post(self, request, *args, **kwargs):
        data = request.FILES.get('data')
        if not data:
            self.message = 'data required'
            self.status_code = ERROR_DATA
            return self.render_to_response({})
        lines = data.read().decode('utf-8').split('\n')
        for line in lines[1:]:
            line = line.split(',')
            vid, level = line[0], line[-1]
            print vid, level
            try:
                video = Video.objects.get(id=vid)
                video.level = level
                video.save()
            except Exception as e:
                continue
        return self.render_to_response({})


class ChangeVideoOrderView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Video
    queryset = None

    def get(self, request, *args, **kwargs):
        change_list = Video.objects.filter(change=True)
        for itm in change_list:
            itm.change = False
            itm.order = 0
            itm.like = 0
            itm.save()

        for i in range(1, 6):
            self.change_order(i)

        self.queryset = Video.objects.filter(level=1)
        for i in range(10):
            obj = self.get_random_item()
            if obj:
                obj.like = 10000
                obj.change = True
                obj.save()

    def change_order(self, classification):
        self.queryset = Video.objects.filter(classification=classification, level=1)
        for i in range(7):
            obj = self.get_random_item()
            if obj:
                obj.order = 100
                obj.change = True
                obj.save()
        self.queryset = Video.objects.filter(classification=classification, level=2)
        for i in range(2):
            obj = self.get_random_item()
            if obj:
                obj.order = 90
                obj.change = True
                obj.save()
        self.queryset = Video.objects.filter(classification=classification, level=3)
        for i in range(1):
            obj = self.get_random_item()
            if obj:
                obj.order = 80
                obj.change = True
                obj.save()

    def get_random_item(self):
        count = self.queryset.count() - 1
        if count:
            index = random.randint(0, count)
            return self.queryset[index]
        return None
