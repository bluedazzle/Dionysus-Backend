from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Dionysus.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^site_admin/', include(admin.site.urls)),
                       url(r'^admin/', include('myadmin.urls')),
                       url(r'^api/v1/', include('api.urls')),
                       )
