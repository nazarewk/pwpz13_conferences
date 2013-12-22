# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from filer.fields.file import FilerFileField
import random
import string

User = settings.AUTH_USER_MODEL


class TimePeriod(models.Model):
    '''
    Class representing time periods with description, start date and either
     end date or length
    '''
    description = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    use_length = models.BooleanField(
        default=False,
        help_text=_( 'Should use length instead of end date?'))
    length = models.PositiveIntegerField(help_text=_('Length in minutes'))

    # 'conference_durations' = FK(Conference)
    # 'summaries_submissions' = FK(Conference)
    # 'publications_submissions' = FK(Conference)
    # 'registration_periods' = MM(Conference)
    # 'sessions_dates' = FK(Session)
    # 'lectures_dates' = FK(Lecture)
    # 'payments' = FK(Payment)


class Conference(models.Model):
    site = models.OneToOneField(Site)
    admins = models.ManyToManyField(User)

    name = models.CharField(max_length=256)

    duration = models.ForeignKey(
        TimePeriod, related_name='conference_durations')
    summaries_submission_period = models.ForeignKey(
        TimePeriod, related_name='summaries_submissions')
    # 'summaries' = FK(Summary)
    publications_submission_period = models.ForeignKey(
        TimePeriod, related_name='publications_submissions')
    # 'sessions__lectures__publications'
    registration_periods = models.ManyToManyField(
        TimePeriod, related_name='registration_periods')


class ConferencesFile(models.Model):
    '''
    Multi-table inheritance base model

    https://docs.djangoproject.com/en/1.6/topics/db/models/#multi-table-inheritance
    '''

    author = models.ForeignKey(User)
    file = FilerFileField()
    status = models.CharField(max_length=2, choices=(
        ('W8', _('Waiting')),
        ('OK', _('Accepted')),
        ('NO', _('Rejected')),
        ('ER', _('Spam')),
    ))
    extra_info = models.CharField(max_length=128)


class Summary(ConferencesFile):
    '''
    Represents summaries to accept for further lectures during conference
    '''
    conference = models.ForeignKey(Conference, related_name='summaries')


class Publication(ConferencesFile):
    '''
    Represents post-conference publications related to given lectures
    '''
    lecture = models.ForeignKey('Lecture', related_name='publications')


class Reviewer(models.Model):
    '''
    Represents both out-of-system and in-system reviewers including
        availability information
    '''
    user_account = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254) # RFC3696/5321-compliant length
    contact_phone = models.CharField(max_length=64)

    is_retired = models.BooleanField(default=False)

    # reviewers available by default for 30 days
    available_until = models.DateTimeField(default=lambda d:
    timezone.now() + timedelta(days=30))

    def is_available(self):
        return not self.is_retired and self.available_until > timezone.now()


class Review(models.Model):
    '''
    Represents review of lecture summaries and publications
    '''
    reviewer = models.ForeignKey(Reviewer)
    file_reviewed = models.ForeignKey(ConferencesFile)

    unguessable_id_length = 32
    unguessable_id = models.CharField(
        max_length=unguessable_id_length, unique=True,
        default=lambda: Review._next_unguessable_id())

    accepted = models.BooleanField()
    comment = models.TextField(blank=True)

    # should become uneditable after accepted
    editable = models.BooleanField(default=True)

    @staticmethod
    def _next_unguessable_id():
        while True:
            # generate random sequence of letters + numbers
            rnd_str = ''.join(
                random.choice(string.ascii_letters + string.digits)
                for x in range(Review.unguessable_id_length))
            if not Review.objects.exists(unguessable_id=rnd_str):
                return rnd_str


class Topic(models.Model):
    '''
    Class represents topics structure of the conference,
     topics without super_topic are the most general
    '''
    conference = models.ForeignKey(Conference)
    name = models.CharField(max_length=256)
    super_topic = models.ForeignKey('self', null=True, blank=True,
                                    related_name='sub_topics')


class Session(models.Model):
    '''
    Represents sessions assigned to given root/sub topics,
     admin of super-topic session should be also admin of all sub-sessions
    '''
    conference = models.ForeignKey(Conference,
                                   related_name='sessions')
    admins = models.ManyToManyField(User)
    topic = models.OneToOneField(Topic)

    name = models.CharField(max_length=256)
    duration = models.ForeignKey(
        TimePeriod, related_name='sessions_dates')


class Lecture(models.Model):
    '''
    Represents single speech during the session,
     Lectures are based upon reviewed and accepted summaries
     Lectures can have post-conference publications
    '''
    session = models.ForeignKey(Session, related_name='lectures')
    referents = models.ManyToManyField(User)
    summary = models.OneToOneField(Summary)
    # 'publications' = FK(Publication)

    duration = models.ForeignKey(
        TimePeriod, related_name='lectures_dates')


class Balance(models.Model):
    user = models.ForeignKey(User)


class Payment(models.Model):
    balance = models.ForeignKey(Balance)
    short_description = models.CharField(max_length=128)
    full_description = models.TextField(blank=True)

    time_to_pay = models.ForeignKey(
        TimePeriod, related_name='payments')

    currency = models.CharField(max_length=3, choices=(
        ('PLN', 'Złote polskie'),
    ))
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    paid = models.DecimalField(max_digits=10, decimal_places=3)


