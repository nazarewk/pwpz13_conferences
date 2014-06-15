# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import os
import string
from datetime import datetime, timedelta, MAXYEAR, MINYEAR

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.managers import CurrentSiteManager
from django.db.models import Q, Manager
from django.db.models.query import EmptyQuerySet
from django.db.models.signals import post_save
from django.utils.timezone import utc
from django.utils.translation import ugettext as _
from django.db import models, OperationalError
from django.contrib.sites.models import Site
from django.utils import timezone
from filer.models import File, Folder


FILE_STATUSES = (
    ('PR', _('Oczekuje')),
    ('RD', _('Gotowy')),  # Ready for admin's decision to accept or reject
    ('OK', _('Akceptowany')),
    ('NO', _('Odrzucony')),
    ('IQ', _('Sporny')),
    ('ER', _('Spam')),
)

REVIEW_STATUSES = (
    ('NO', _('Oczekuje')),
    ('OK', _('Zaakceptowane')),  # Ready for admin's decision to accept or reject
    ('RE', _('Odrzucone')),
)


class TimePeriod(models.Model):
    """
    Class representing time periods with description, start date and either
     end date or length
    """
    description = models.CharField(max_length=128, blank=True, verbose_name=_('Opis'))
    start = models.DateTimeField(verbose_name=_('Początek'))
    end = models.DateTimeField(verbose_name=_('Koniec'))

    # 'conference_duration' = 11(Conference)
    # 'summaries_submission' = 11(Conference)
    # 'publications_submission' = 11(Conference)
    # 'registration_periods' = MM(Conference)
    # 'sessions_date' = 11(Session)
    # 'lectures_date' = 11(Lecture)
    # 'payment' = 11(Payment)
    # 'reviewer_availability' = MM(Reviewer)
    # 'reviewer_unavailability' = MM(Reviewer)

    def __unicode__(self):
        return '%s: %s - %s' % (self.description, self.start.strftime('%Y-%m-%d %H:%M'),
                                self.end.strftime('%Y-%m-%d %H:%M'))

    def get_duration(self):
        """
        Returns datetime.timedelta representing duration
        """
        return self.end - self.start

    def is_now(self):
        now = datetime.now()
        return self.start <= now and now <= self.end

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
    site = models.OneToOneField(Site, null=True, blank=True)
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name='conference_admins')
    registered_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name='conference_registered_users')

    name = models.CharField(max_length=256)

    duration = models.OneToOneField(
        TimePeriod, related_name='conference_duration',
        null=True, blank=True)
    summaries_submission_period = models.OneToOneField(
        TimePeriod, related_name='summaries_submission',
        null=True, blank=True)
    # 'summaries' = FK(Summary)
    publications_submission_period = models.OneToOneField(
        TimePeriod, related_name='publications_submission',
        null=True, blank=True)
    # 'sessions__lectures__publications'
    registration_periods = models.ManyToManyField(
        TimePeriod, related_name='registration_periods',
        null=True, blank=True)

    objects = Manager()

    def __unicode__(self):
        return self.name

    @classmethod
    def get_sessions(cls):
        c = cls.get_current()
        return c.sessions if c else EmptyQuerySet

    @classmethod
    def get_current(cls):
        ret, created = None, None
        try:
            ret, created = cls.objects.get_or_create(defaults={
                'name': _('Default conference'),
            }, site__id=settings.SITE_ID)
        except OperationalError:
            ret = Conference(name=_('Empty conference'))
            created = True
            ret.save()
        if created:
            start = datetime.utcnow().replace(tzinfo=utc)
            duration = timedelta(days=365)
            tp = TimePeriod(start=start, end=start + duration)
            tp.save()
            ret.duration = tp
            tp = TimePeriod(start=start, end=start + duration)
            tp.save()
            ret.summaries_submission_period = tp
            tp = TimePeriod(start=start, end=start + duration)
            tp.save()
            ret.publications_submission_period = tp
            tp = TimePeriod(start=start, end=start + duration)
            tp.save()
            ret.registration_periods.add(tp)
            ret.site_id = settings.SITE_ID
            ret.save()
        return ret

    @classmethod
    def is_admin(cls, user):
        c = cls.get_current()
        return c.admins.filter(pk=user.pk).exists() if c else False


class ConferencesFile(File):
    """
    Multi-table inheritance base model

    https://docs.djangoproject.com/en/1.6/topics/db/models/#multi-table-inheritance
    """
    filename_extensions = []
    folder_path = ['conferences', 'files']

    status = models.CharField(max_length=2,
                              choices=FILE_STATUSES,
                              default='PR')

    def save(self, *args, **kwargs):
        # self.folder = Folder.objects.create(name="root folder", parent=None)
        if not self.folder:
            folder = None
            for name in self.folder_path:
                folder, _ = Folder.objects.get_or_create(
                    name=name,
                    parent=folder)
            self.folder = folder
        super(ConferencesFile, self).save(*args, **kwargs)

    # Properties for backwards compatibility
    @property
    def author(self):
        return self.owner

    @author.setter
    def author(self, value):
        self.owner = value

    @property
    def extra_info(self):
        return self.description

    @extra_info.setter
    def extra_info(self, value):
        self.description = value

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        ext = os.path.splitext(iname)[1].lower()
        return ext in cls.filename_extensions if cls.filename_extensions else True

    @property
    def status_verbose(self):
        return get_display(self.status, FILE_STATUSES)


class Summary(ConferencesFile):
    """
    Represents summaries to accept for further lectures during conferences
    """
    filename_extensions = ['.pdf', '.txt']
    folder_path = ['conferences', 'summaries']
    conference = models.ForeignKey(
        Conference,
        default=lambda: Conference.get_current(),
        related_name='summaries',
        verbose_name=_('Konferencja'))


class Reviewer(models.Model):
    """
    Represents both out-of-system and in-system reviewers including
        availability information
    """
    user_account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        verbose_name=_('Konto użytkownika'))
    title = models.CharField(
        null=True, blank=True,
        max_length=64,
        verbose_name=_('Tytuł'))
    first_name = models.CharField(
        null=True, blank=True,
        max_length=64,
        verbose_name=_('Imię'))
    last_name = models.CharField(
        null=True, blank=True,
        max_length=64,
        verbose_name=_('Nazwisko'))
    email = models.EmailField(
        null=True, blank=True,
        max_length=254,
        verbose_name=_('Email'))  # RFC3696/5321-compliant length
    contact_phone = models.CharField(
        null=True, blank=True,
        max_length=64,
        verbose_name=_('Telefon'))

    is_active = models.BooleanField(default=True, verbose_name=_('Aktywny'))

    availability = models.ManyToManyField(
        TimePeriod,
        related_name='reviewer_availability',
        verbose_name=_('Dostępność'))
    unavailability = models.ManyToManyField(
        TimePeriod,
        related_name='reviewer_unavailability',
        verbose_name=_('Niedostępność'))

    def is_available(self, from_date=timezone.now(), for_days=0):
        """
        Returns true if reviewer is available for given number of days starting
         with specified date.
        By default returns true if reviewer is available right now
        """
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

        if (self.user_account):
            return
        if not self.title:
            error_messages.append(ValidationError(_('Tytuł jest wymagany!')))
        if not self.first_name:
            error_messages.append(ValidationError(_('Imię jest wymagane!')))
        if not self.last_name:
            error_messages.append(ValidationError(_('Nazwisko jest wymagane!')))
        if not self.email:
            error_messages.append(ValidationError(_('Email jest wymagany!')))
        if ( len(error_messages) > 0):
            raise ValidationError(error_messages)

    def name(self):
        if (self.user_account):
            if (self.user_account.first_name or self.user_account.last_name):
                return '%s %s' % (
                    self.user_account.first_name, self.user_account.last_name)
            else:
                return self.user_account.username
        else:
            return '%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.name()


class Review(models.Model):
    """
    Represents review of lecture summaries and publications
    """
    reviewer = models.ForeignKey(Reviewer, verbose_name=_('Recenzent'))
    file_reviewed = models.ForeignKey(ConferencesFile, verbose_name=_('Plik do recenzji'))

    # unguessable ID for use in urls
    unguessable_id_length = 32
    unguessable_id = models.CharField(
        max_length=unguessable_id_length, unique=True,
        default=lambda: Review._next_unguessable_id())

    status = models.CharField(max_length=2,
                              choices=REVIEW_STATUSES,
                              default='NO')
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
            if not Review.objects.filter(unguessable_id=rnd_str).exists():
                return rnd_str

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        file = self.file_reviewed
        if file.review_set.filter(status='OK').count() == 1 and file.review_set.filter(status='RE').count()==1:
            file.status = 'IQ'
        elif file.review_set.filter(status='OK').count() >= 2:
            file.status = 'OK'
        elif file.review_set.filter(status='RE').count() >= 1:
            file.status = 'NO'
        else:
            file.status = 'PR'
        file.save()


class Topic(models.Model):
    """
    Class represents topics structure of the conferences,
     topics without super_topic are the most general
    """
    conference = models.ForeignKey(
        Conference,
        default=lambda: Conference.get_current(),
        related_name='topics',
        verbose_name="Konferencja")
    name = models.CharField(max_length=256, verbose_name="Nazwa")
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        related_name='children',
        verbose_name="Temat nadrzędny")

    def __unicode__(self):
        return self.name


class Session(models.Model):
    """
    Represents sessions assigned to given root/sub topics,
     admin of super-topic session should be also admin of all sub-sessions
    """
    conference = models.ForeignKey(
        Conference,
        default=lambda: Conference.get_current(),
        related_name='sessions',
        verbose_name=_('Konferencja'))
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Admini'),
        related_name='session_admins')
    registered_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name='session_registered_users')
    topic = models.OneToOneField(Topic, verbose_name=_('Temat'))

    name = models.CharField(max_length=256, verbose_name=_('Nazwa'))

    duration = models.ForeignKey(
        TimePeriod, related_name='sessions_dates', verbose_name=_('Czas trwania'))

    def __unicode__(self):
        return self.name

    def is_admin(self, user):
        return self.admins.filter(pk=user).exists()


class Lecture(models.Model):
    """
    Represents single speech during the session,
     Lectures are based upon reviewed and accepted summaries
     Lectures can have post-conferences publications
    """
    title = models.CharField(max_length=256, verbose_name=_('Tytuł'))
    session = models.ForeignKey(Session, related_name='lectures', verbose_name=_('Sesja'))
    referents = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Referenci'))
    summary = models.OneToOneField(Summary, verbose_name=_('Streszczenie'))
    # 'publications' = FK(Publication)

    duration = models.OneToOneField(
        TimePeriod, related_name='lectures_dates', verbose_name=_('Czas trwania'))

    def __unicode__(self):
        return self.title


class Publication(ConferencesFile):
    """
    Represents post-conferences publications related to given lectures
    """
    filename_extensions = ['.pdf', '.txt']
    folder_path = ['conferences', 'publications']
    lecture = models.ForeignKey(Lecture, related_name='publications', verbose_name=_('Referat'))


class Balance(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Użytkownik'),
        related_name='balance')
    available = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Dostępne środki'),
        default=0)
    is_student = models.BooleanField(default=False, verbose_name=_('Czy jest studentem?'))

    def set_paid(self, payment):
        if self.available < payment.amount:
            return False
        self.available -= payment.amount
        payment.is_paid = True
        payment.save()
        self.save()
        return True

    @staticmethod
    def add_user_balance(sender, instance, **kwargs):
        b, created = Balance.objects.get_or_create(user=instance)

    def __unicode__(self):
        return '%s - %.2f PLN' % (self.user, self.available)


class Payment(models.Model):
    balance = models.ForeignKey(
        Balance,
        verbose_name=_('Saldo'),
        related_name='payments')
    short_description = models.CharField(
        max_length=128,
        verbose_name=_('Krótki opis płatności'))
    full_description = models.TextField(
        blank=True,
        verbose_name=_('Pełny opis płatności'))

    time_to_pay = models.OneToOneField(
        TimePeriod, related_name='payment', verbose_name=_('Termin zapłaty'))

    currency = models.CharField(max_length=3, choices=(
        ('PLN', _('Złote polskie'), ),
    ), verbose_name=_('Waluta'), default='PLN')
    amount = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_('Kwota płatności'))

    is_paid = models.BooleanField(_('Czy zapłacono?'), default=False)

    summary = models.OneToOneField(
        Summary,
        verbose_name=_('Za streszczenie (referat)'),
        related_name='payment',
        blank=True, null=True
    )

    is_confirmed = models.BooleanField(_('Czy jest potwierdzona?'), default=False)

    def set_paid(self):
        self.balance.set_paid(self)

    def __unicode__(self):
        return '[%s %.2f %s] %s' % (self.balance.user, self.amount, self.currency, self.short_description)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    activation_key = models.CharField(
        max_length=40,
        unique=True,
        blank=True,
        null=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.activation_key:
            key = ''
            while True:
                key = ''.join([
                    random.choice(string.ascii_letters + string.digits)
                    for i in range(self._meta.get_field_by_name(
                        'activation_key')[0].max_length)
                ])
                if not UserProfile.objects.filter(activation_key=key).exists():
                    break
            self.activation_key = key
        super(UserProfile, self).save(*args, **kwargs)

    def name(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    @staticmethod
    def add_user_profile(sender, instance, **kwargs):
        o, created = UserProfile.objects.get_or_create(user=instance)


class Price(models.Model):
    conference = models.ForeignKey(
        Conference,
        default=lambda:Conference.get_current(),
        related_name='pricing')
    title = models.CharField(
        verbose_name=_('Krótki opis'),
        max_length=128)
    description = models.TextField(
        verbose_name=_('Pełny opis'),
        blank=True)
    value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Wartość'),
        default=0)

    def __unicode__(self):
        return '[%.2f] %s' % (self.value, self.title)

    def get_all_current(self):
        return


def get_display(key, list):
    d = dict(list)
    if key in d:
        return d[key]
    return None


post_save.connect(Balance.add_user_balance, sender=get_user_model())
post_save.connect(UserProfile.add_user_profile, sender=get_user_model())