from django.conf.urls import patterns, include, url
from django.contrib import admin

from Dionysus import settings
from Dionysus.sitemap import ShareSitemap
from page.views import AppRedirectView, AppAboutView

sitemaps = {
    'share': ShareSitemap,
}

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', AppRedirectView.as_view()),
                       url(r'^about/$', AppAboutView.as_view()),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^site_admin/', include(admin.site.urls)),
                       url(r'^admin/api/', include('myadmin.api_urls')),
                       url(r'^admin/', include('myadmin.urls')),
                       url(r'^api/v1/', include('api.urls')),
                       url(r'^page/', include('page.urls')),
                       url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                       url(r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA}),
                       )
