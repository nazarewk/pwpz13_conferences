from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from conferences.views import ReviewerListView
from conferences.views import ReviewerDetailView

urlpatterns = patterns(
    '',
    url(
        r'^$',
        "conferences.views.home",
        name="home"
    ),

    #reviewers urls section
    url(
        r'^reviewers/$',
        ReviewerListView.as_view(),
        name="reviewer_list"
    ),
    url(
        r'^reviewers/(?P<pk>\d+)/$',
        ReviewerDetailView.as_view(),
        name="reviewer_detail"
    ),
)