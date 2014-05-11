# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.db import models
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone
from django import forms
from datetime import datetime, timedelta, MAXYEAR, MINYEAR
from filer.fields.file import FilerFileField

import random
import string

User = get_user_model()


class TimePeriod(models.Model):
    '''
    Class representing time periods with description, start date and either
     end date or length
    '''
    description = models.CharField(max_length=128, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    # 'conference_durations' = FK(Conference)
    # 'summaries_submissions' = FK(Conference)
    # 'publications_submissions' = FK(Conference)
    # 'registration_periods' = MM(Conference)
    # 'sessions_dates' = FK(Session)
    # 'lectures_dates' = FK(Lecture)
    # 'payments' = FK(Payment)
    # 'reviewer_availability' = MM(Reviewer)
    # 'reviewer_unavailability' = MM(Reviewer)

    def __str__(self):
        return '%s - %s' %(self.start.strftime('%Y-%m-%d %H:%M:%S'), self.end.strftime('%Y-%m-%d %H:%M:%S'))

    def get_duration(self):
        '''
        Returns datetime.timedelta representing duration
        '''
        return self.end - self.start

    @staticmethod
    def are_continuous(
            time_periods_query_set,
            from_date=datetime(MINYEAR, 1, 1),
            to_date=datetime(MAXYEAR, 1, 1)):
        time_periods_query_set = time_periods_query_set.order_by('start')
        last_end = from_date
        for tp in time_periods_query_set:
            if tp.start > to_date:
                break
            if last_end < tp.end:
                last_end = tp.end
            if last_end < tp.start:
                return False
        return True


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

    def __str__(self):
        return self.name


class ConferencesFile(models.Model):
    '''
    Multi-table inheritance base model

    https://docs.djangoproject.com/en/1.6/topics/db/models/#multi-table-inheritance
    '''

    author = models.ForeignKey(User)
    file = FilerFileField()
    status = models.CharField(max_length=2, choices=(
        ('PR', _('Processing')),
        ('RD', _('Ready')), # Ready for admin's decision to accept or reject
        ('OK', _('Accepted')),
        ('NO', _('Rejected')),
        ('ER', _('Spam')),
    ))
    extra_info = models.CharField(max_length=128)


class Summary(ConferencesFile):
    '''
    Represents summaries to accept for further lectures during conferences
    '''
    conference = models.ForeignKey(Conference, related_name='summaries')


class Publication(ConferencesFile):
    '''
    Represents post-conferences publications related to given lectures
    '''
    lecture = models.ForeignKey('Lecture', related_name='publications')


class Reviewer(models.Model):
    '''
    Represents both out-of-system and in-system reviewers including
        availability information
    '''
    user_account = models.ForeignKey(User, null=True, blank=True,verbose_name=u"Konto użytkownika")
    title = models.CharField(null=True, blank=True,max_length=64,verbose_name=u"Tytuł")
    first_name = models.CharField(null=True, blank=True,max_length=64,verbose_name=u"Imię")
    last_name = models.CharField(null=True, blank=True,max_length=64,verbose_name=u"Nazwisko")
    email = models.EmailField(null=True, blank=True,max_length=254,verbose_name=u"Email") # RFC3696/5321-compliant length
    contact_phone = models.CharField(null=True, blank=True,max_length=64,verbose_name=u"Telefon")

    is_active = models.BooleanField(default=True,verbose_name=u"Aktywny")

    availability = models.ManyToManyField(
        TimePeriod, related_name='reviewer_availability',verbose_name=u"Dostępność")
    unavailability = models.ManyToManyField(
        TimePeriod, related_name='reviewer_unavailability',verbose_name=u"Niedostępność")

    def is_available(self, from_date=timezone.now(), for_days=0):
        '''
        Returns true if reviewer is available for given number of days starting
         with specified date.
        By default returns true if reviewer is available right now
        '''
        to_date = from_date + timedelta(days=for_days)
        # Q object info:
        # https://docs.djangoproject.com/en/1.6/topics/db/queries/#complex-lookups-with-q-objects

        return self.unavailability.filter(
            Q(start__gt=to_date) | Q(end__lt=from_date)
        ).exists() and TimePeriod.are_continuous(
            self.availability.filter(
                Q(start__lt=from_date) | Q(end__gt=to_date)),
            from_date,
            to_date
        )

    def clean(self):
        error_messages = []
        from django.core.exceptions import ValidationError
        if(self.user_account):
            return
        if not self.title:
            error_messages.append(ValidationError('Tytuł jest wymagany!'))
        if not self.first_name:
            error_messages.append(ValidationError('Imię jest wymagane!'))
        if not self.last_name:
            error_messages.append(ValidationError('Nazwisko jest wymagane!'))
        if not self.email:
            error_messages.append(ValidationError('Email jest wymagany!'))
        if( len(error_messages)>0):
            raise ValidationError(error_messages)

    def name(self):
        if(self.user_account):
			if(self.user_account.first_name or self.user_account.last_name):
				return "%s %s" % (self.user_account.first_name, self.user_account.last_name)
			else:
				return self.user_account.username
        else:
            return "%s %s" % (self.first_name, self.last_name)

class Review(models.Model):
    '''
    Represents review of lecture summaries and publications
    '''
    reviewer = models.ForeignKey(Reviewer)
    file_reviewed = models.ForeignKey(ConferencesFile)

    # unguessable ID for use in urls
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
    Class represents topics structure of the conferences,
     topics without super_topic are the most general
    '''
    conference = models.ForeignKey(Conference)
    name = models.CharField(max_length=256)
    super_topic = models.ForeignKey('self', null=True, blank=True,
                                    related_name='sub_topics')

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name


class Lecture(models.Model):
    '''
    Represents single speech during the session,
     Lectures are based upon reviewed and accepted summaries
     Lectures can have post-conferences publications
    '''
    session = models.ForeignKey(Session, related_name='lectures')
    referents = models.ManyToManyField(User)
    summary = models.OneToOneField(Summary)
    # 'publications' = FK(Publication)

    duration = models.ForeignKey(
        TimePeriod, related_name='lectures_dates')




class Balance(models.Model):
    user = models.ForeignKey(User)
    is_student = models.BooleanField(default=False)


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


class ReviewerForm(ModelForm):
    class Meta:
        model=Reviewer
        fields = ['user_account','first_name','last_name','email','title','contact_phone','availability']


class SessionForm(ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the session name")
    duration = forms.ModelChoiceField(queryset=TimePeriod.objects.all(), help_text="Please choose duration of session")
    conference = forms.ModelChoiceField(queryset=Conference.objects.all(), help_text="Please choose conference")
    topic = forms.ModelChoiceField (queryset=Topic.objects.all(), help_text="Please choose session topic")
    admins = forms.ModelMultipleChoiceField (queryset=User.objects.all())
    admins.help_text = 'Please choose Admin'

    class Meta:
        model = Session

class TimePeriodForm(ModelForm):
    description = forms.CharField(max_length=128, help_text="Please enter the description of the Time Period")
    start = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    end = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    class Meta:
        model = TimePeriod

    def __init__(self, *args, **kwargs):
        super(TimePeriodForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = widgets.AdminSplitDateTime()
        self.fields['end'].widget = widgets.AdminSplitDateTime()


class LectureForm(ModelForm):

    class Meta:
        model = Lecture