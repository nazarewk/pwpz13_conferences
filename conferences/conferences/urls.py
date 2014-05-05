from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }
    ),
    url(
        r'^$',
        "conferences.views.home",
        name="home"
    ),
)

#reviewers urls section

urlpatterns += patterns(
    "conferences.views",
    url(
        r'^reviewers/$',
        "reviewer_list"
    ),
    url(
        r'^reviewers/(?P<pk>\d+)/$',
        "reviewer_detail",
    ),
    url(
        r'^reviewers/add$',
        "reviewer_create"
    ),
    url(
        r'^reviewers/(?P<pk>\d+)/edit$',
        "reviewer_edit",
    ),
    url(
        r'^reviewers/(?P<pk>\d+)/remove$',
        "RetireReviewer",
    ),
)

urlpatterns += patterns("conferences.views",
    url(r'^sessions/(?P<pk>\d+)/$', "session"),
    url(r'^sessions/add/$', "add_session"),
    url(r'^sessions/$', "session_list"),
    url(r'^sessions/edit/(?P<pk>\d+)/$', "edit_session"),
    url(r'^sessions/delete/(?P<pk>\d+)/$', "remove_session"),

)
