# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from . import models
from .models import Session, Conference, TimePeriod,Summary

class FilterForm(forms.Form):
    FILTERS=[('', _('Wszystkie')),
             ('accepted', _('Zaakceptowane')),
             ('waiting', _('Oczekujące')),
             ('rejected', _('Odrzucone')),
             ('questionable', _('Sporne')),
             ]
    filter=forms.ChoiceField(choices=FILTERS,
                                  widget=forms.RadioSelect(),
                                  label='Filtry',
                                  required=False)

class ReviewerForm(forms.ModelForm):
    class Meta:
        model = models.Reviewer
        fields = ['user_account', 'first_name', 'last_name', 'email', 'title',
                  'contact_phone']

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['reviewer', 'file_reviewed']

class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['status','comment']

class TopicForm(forms.ModelForm):
    class Meta:
        model = models.Topic


class SessionForm(forms.ModelForm):
    admins = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(), label='Admini')
    admins.help_text = ''

    class Meta:
        model = models.Session
        fields = ['name', 'duration', 'conference', 'topic', 'admins']


class TimePeriodForm(forms.ModelForm):
    start = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label='Początek')
    end = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label='Koniec')

    class Meta:
        model = models.TimePeriod
        fields = ['description', 'start', 'end', ]

    def __init__(self, *args, **kwargs):
        super(TimePeriodForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = widgets.AdminSplitDateTime()
        self.fields['end'].widget = widgets.AdminSplitDateTime()


class LectureForm(forms.ModelForm):
    start = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label='Początek')
    end = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label='Koniec')

    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)
        self.fields['session'].queryset=Conference.get_sessions()
        if self.instance.id:
            self.fields['start'].initial=self.instance.duration.start
            self.fields['end'].initial=self.instance.duration.end
        else:
            self.fields['summary'].queryset=Summary.objects.filter(conference=Conference.get_current(), lecture=None)
        self.fields['start'].widget = widgets.AdminSplitDateTime()
        self.fields['end'].widget = widgets.AdminSplitDateTime()


    def save(self, commit=True):
        lecture = super(LectureForm, self).save(commit=False)
        if lecture.duration_id:
            tp=TimePeriod.objects.get(pk=lecture.duration.pk)
            tp.start=self.cleaned_data['start']
            tp.end=self.cleaned_data['end']
        else:
            tp = TimePeriod(start=self.cleaned_data['start'], end=self.cleaned_data['end'])
        tp.save()
        lecture.duration = tp
        lecture.save()

    class Meta:
        model = models.Lecture
        fields = ['session', 'title', 'referents', 'summary',]


class UserForm(forms.ModelForm):
    email_errors = {
        'required': 'To pole jest wymagane.',
        'invalid': 'Adres e-mail jest niepoprawny',
    }
    username = forms.CharField(label='Nazwa użytkownika')
    first_name = forms.CharField(required=True, label='Imię')
    last_name = forms.CharField(required=True, label='Nazwisko')
    email = forms.CharField(required=True, label='E-mail',
                            error_messages=email_errors)
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło',
                               min_length=8)

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.exclude(pk=self.instance.pk).filter(
                username=username).exists():
            raise forms.ValidationError(
                'Nazwa użytkownika "%s" jest już w użyciu.' % username)
        return username

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class SummaryForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = models.Summary
        fields = ['conference', 'description']

    def clean(self):
        error_messages = []
        cleaned_data = super(SummaryForm, self).clean()
        conference = cleaned_data.get("conference")
        description = cleaned_data.get("description")
        summary_file = cleaned_data.get("file")

        if conference:
            start = conference.summaries_submission_period.start.replace(tzinfo=None)
            end = conference.summaries_submission_period.end.replace(tzinfo=None)
            if not (start <= datetime.now() <= end):
                error_messages.append(ValidationError(_('Minął czas nadsyłania streszczeń.')))
        if not conference:
            error_messages.append(ValidationError(_('Musisz podać konferencję.')))
        if not description:
            error_messages.append(ValidationError(_('Musisz podać opis streszczenia.')))
        if not summary_file:
            error_messages.append(ValidationError(_('Musisz podać plik ze streszczeniem.')))
        if len(error_messages) > 0:
            raise ValidationError(error_messages)
        return cleaned_data

class SummaryUpdateForm(forms.ModelForm):
    editable=forms.BooleanField(label="Pozwalaj recenzować",required=False)

    class Meta:
        model = models.Summary
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(SummaryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['editable'].initial = self.instance.review_set.filter(editable=True).exists()

    def save(self):
        super(SummaryUpdateForm, self).save()
        if self.cleaned_data['editable'] is False:
            self.instance.review_set.update(editable=self.cleaned_data['editable'])

class PublicationCreateForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = models.Publication
        fields = ['lecture', 'description']

    def clean(self):
        error_messages = []
        from django.core.exceptions import ValidationError
        cleaned_data = super(PublicationCreateForm, self).clean()
        lecture = cleaned_data.get("lecture")
        description = cleaned_data.get("description")
        publication_file = cleaned_data.get("file")

        if lecture:
            conference = lecture.session.conference
            start = conference.publications_submission_period.start.replace(tzinfo=None)
            end = conference.publications_submission_period.end.replace(tzinfo=None)
            if not (start <= datetime.now() <= end):
                error_messages.append(ValidationError(_('Minął czas nadsyłania publikacji.')))
        if not lecture:
            error_messages.append(ValidationError(_('Musisz podać referat.')))
        if not description:
            error_messages.append(ValidationError(_('Musisz podać opis referatu.')))
        if not publication_file:
            error_messages.append(ValidationError(_('Musisz podać plik z referatem.')))
        if len(error_messages) > 0:
            raise ValidationError(error_messages)
        return cleaned_data

class PublicationUpdateForm(forms.ModelForm):
    editable=forms.BooleanField(label="Pozwalaj recenzować",required=False)

    class Meta:
        model = models.Publication
        fields = ['status',]

    def __init__(self, *args, **kwargs):
        super(PublicationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['editable'].initial = self.instance.review_set.filter(editable=True).exists()

    def save(self):
        super(PublicationUpdateForm, self)
        if self.cleaned_data['editable'] is False:
            self.instance.review_set.update(editable=self.cleaned_data['editable'])

class SendingEmailForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  label=_('Nazwa użytkownika'),
                                  required=True)
    subject = forms.CharField(max_length=30,
                              label=_('Temat'),
                              required=True)
    message = forms.CharField(max_length=500, widget=forms.Textarea,
                              label=_('Treść'),
                              required=True)


class SendingEmailsForm(forms.Form):
    CHOICES = [('reviewers', _('Recenzenci')),
               ('users', _('Użytkownicy'))]
    sessions = Session.objects.all()
    for session in sessions:
        CHOICES.append((session.name, _('Admini sesji: %s') % session.name))

    group = forms.MultipleChoiceField(choices=CHOICES,
                                      widget=forms.CheckboxSelectMultiple(),
                                      label=_('Grupy'),
                                      required=True)
    subject = forms.CharField(max_length=30,
                              label=_('Temat'),
                              required=True)
    message = forms.CharField(max_length=500, widget=forms.Textarea,
                              label=_('Treść'),
                              required=True)


class AccountForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label='Obecne hasło')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='Nowe hasło', min_length=8)
    repeat_new_password = forms.CharField(widget=forms.PasswordInput(), label='Powtórz hasło')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AccountForm, self).__init__(*args, **kwargs)

    def clean(self):
        error_messages = []
        from django.core.exceptions import ValidationError
        cleaned_data = super(AccountForm, self).clean()
        old = cleaned_data.get("old_password")
        new = cleaned_data.get("new_password")
        repeated = cleaned_data.get("repeat_new_password")

        if old and new and repeated:
            if not self.user.check_password(old):
                error_messages.append(ValidationError(_('Obecne hasło jest niepoprawne.')))
            if new != repeated:
                error_messages.append(ValidationError(_('Podane hasła różnią się.')))
            if ( len(error_messages) > 0):
                raise ValidationError(error_messages)