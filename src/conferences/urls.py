from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
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


# reviewers urls section

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
    url(r'^reviews/$',
        views.review_list,
        name='review-list'
    ),
    url(r'^reviews/add$',
        views.review_add,
        name='review-add'
    ),
    url(r'^reviews/add/(?P<file_id>\d+)/$',
        views.review_add,
        name='review-add'
    ),
    url(r'^reviews/edit/(?P<pk>\d+)/$',
        views.review_edit,
        name='review-edit'
    ),
    url(r'^reviews/delete/(?P<pk>\d+)/$',
        views.review_delete,
        name='review-delete'
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
    url(r'^topics/(?P<pk>\d+)/$',
        views.topic_details,
        name='topic-details'
    ),
    url(r'^topics/add/$',
        views.topic_add,
        name='topic-add'
    ),
    url(r'^topics/$',
        views.topic_list,
        name='topic-list'
    ),
    url(r'^topics/edit/(?P<pk>\d+)/$',
        views.topic_edit,
        name='topic-edit'
    ),
    url(r'^topics/delete/(?P<pk>\d+)/$',
        views.topic_delete,
        name='topic-delete'
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

urlpatterns += patterns(
    '',
    url(r'^users/login$',
        views.user_login,
        name='user-login'
    ),
    url(r'^users/registration$',
        views.registration,
        name='user-registration'
    ),
    url(r'^users/logout$',
        views.user_logout,
        name='user-logout'
    ),
    url(r'^users/confirm/(?P<key>\w+)/$',
        views.user_confirm,
        name='user-confirm'
    ),
    url(r'^users/sending/$',
        views.email_send,
        name='email-send'
    ),
    url(r'^users/multi-sending/$',
        views.multi_email_send,
        name='multi-email-send'
    ),
    url(r'^users/account/$',
        views.account,
        name='account'
    ),
)

urlpatterns += patterns(
    '',
    url(r'^summary/add$',
        views.summary_add,
        name='summary-add'
    ),
    url(r'^summaries/$',
        views.summary_list,
        name='summary-list'
    ),
    url(r'^summaries/(?P<pk>\d+)/$',
        views.summary_details,
        name='summary-details'
    ),
    url(r'^summaries/edit/(?P<pk>\d+)/$',
        views.summary_edit,
        name='summary-edit'
    ),
)

urlpatterns += patterns(
    '',
    url(r'^publications/add$',
        views.publication_add,
        name='publication-add'
    ),
    url(r'^publications/$',
        views.publication_list,
        name='publication-list'
    ),
    url(r'^publications/edit/(?P<pk>\d+)/$',
        views.publication_edit,
        name='publication-edit'
    ),
)

urlpatterns += patterns(
    '',
    url(r'^conference-registration',
        views.conference_registration,
        name='conference-registration'
    ),
    url(r'^payments/$',
        views.payments_list,
        name='payments-list'
    ),
    url(r'^payments/(?P<pk>\d+)/pay$',
        views.payments_pay,
        name='payments-pay'
    ),
    url(r'^payments/(?P<pk>\d+)/confirm$',
        views.payment_confirm,
        name='payments-confirm'
    ),
    url(r'^payments/(?P<pk>\d+)/delete$',
        views.payment_delete,
        name='payments-delete'
    ),
)