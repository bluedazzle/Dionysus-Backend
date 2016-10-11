# coding: utf-8
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic import UpdateView, TemplateView, ListView, RedirectView

from myadmin.models import HAdmin
from core.Mixin.CheckMixin import CheckAdminPagePermissionMixin


class AdminView(UpdateView):
    model = HAdmin
    http_method_names = ['get']
    success_url = '/admin/index'

    def get(self, request, *args, **kwargs):
        token = request.session.get('token')
        if token:
            if HAdmin.objects.filter(token=token).exists():
                return HttpResponseRedirect('/admin/video')
        return render_to_response('admin/admin_login.html')


class AdminIndexView(CheckAdminPagePermissionMixin, TemplateView):
    model = HAdmin
    http_method_names = ['get']
    template_name = 'admin/admin_video.html'

    def get(self, request, *args, **kwargs):
        return super(AdminIndexView, self).get(request, *args, **kwargs)


class AdminShareView(CheckAdminPagePermissionMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'admin/admin_share.html'


class AdminLogoutView(CheckAdminPagePermissionMixin, RedirectView):
    url = '/admin/login'
