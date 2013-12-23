from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from conferences.views import ReviewerListView
from conferences.views import ReviewerDetailView


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'conferences_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(
        regex=r'^$',
        view="conferences.views.home",
        name="home"
    ),

    #reviewers urls section
    url(
        regex=r'^reviewers/$',
        view=ReviewerListView.as_view(),
        name="reviewer_list"
    ),
    url(
        regex=r'^reviewers/(?P<pk>\d+)/$',
        view=ReviewerDetailView.as_view(),
        name="reviewer_detail"
    ),
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
