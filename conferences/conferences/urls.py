from django.conf.urls import patterns, url

from conferences import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.home,
        name='home'
    ),
)

# admin datetimepicker urls section
js_info_dict = {
    'packages': ('cui.translations',),
}

urlpatterns += patterns(
    '',
    url(r'^jsi18n/$',
        'django.views.i18n.javascript_catalog',
        js_info_dict),
)


#reviewers urls section

urlpatterns += patterns(
    '',
    url(r'^reviewers/$',
        views.reviewer_list,
        name='reviewer-list'
    ),
    url(r'^reviewers/(?P<pk>\d+)/$',
        views.reviewer_details,
        name='reviewer-details'
    ),
    url(r'^reviewers/add$',
        views.reviewer_create,
        name='reviewer-add'
    ),
    url(r'^reviewers/(?P<pk>\d+)/edit$',
        views.reviewer_edit,
        name='reviewer-edit'
    ),
    url(r'^reviewers/(?P<pk>\d+)/remove$',
        views.reviewer_delete,
        name='reviewer-delete'
    ),
)

urlpatterns += patterns(
    '',
    url(r'^sessions/(?P<pk>\d+)/$',
        views.session_details,
        name='session-details'
    ),
    url(r'^sessions/add/$',
        views.session_add,
        name='session-add'
    ),
    url(r'^sessions/$',
        views.session_list,
        name='session-list'
    ),
    url(r'^sessions/edit/(?P<pk>\d+)/$',
        views.session_edit,
        name='session-edit'
    ),
    url(r'^sessions/delete/(?P<pk>\d+)/$',
        views.session_delete,
        name='session-delete'
    ),
    url(r'^sessions/timeperiod/$',
        views.timeperiod_add,
        name='session-timeperiod-add'
    ),

)

urlpatterns += patterns(
    '',
    url(r'^lectures/(?P<pk>\d+)/$',
        views.lecture_details,
        name='lecture-details'
    ),
    url(r'^lectures/add/$',
        views.lecture_add,
        name='lecture-add'
    ),
    url(r'^lectures/$',
        views.lecture_list,
        name='lecture-list'
    ),
    url(r'^lectures/edit/(?P<pk>\d+)/$',
        views.lecture_edit,
        name='lecture-edit'
    ),
    url(r'^lectures/delete/(?P<pk>\d+)/$',
        views.lecture_delete,
        name='lecture-delete'
    ),
    url(r'^lectures/timeperiod/$',
        views.timeperiod_add,
        name='lecture-timeperiod-add'
    ),
)

urlpatterns += patterns("conferences.views",
    url(r'^users/registration/$', "registration"),
    url(r'^users/logout/$', "user_logout"),
    url(r'^users/confirm/(?P<username>\w+)/(?P<key>\w+)/$', "user_confirm"),

)
