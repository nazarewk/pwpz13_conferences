from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin


admin.autodiscover()

urlpatterns = i18n_patterns(
    '',
    # Examples:
    # url(r'^$', 'conferences_site.views.home', name='pages-root'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^conferences/', include('conferences.urls')),
)

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += patterns(
            '',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
if 'session_security' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'session_security/', include('session_security.urls')),
    )

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    ) + urlpatterns

urlpatterns += i18n_patterns(
    '',
    url(r'^', include('cms.urls')),
)
