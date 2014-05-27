# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets
from django.db.models.query import EmptyQuerySet
from django.utils.translation import ugettext as _

from . import models
from .models import Session, Conference, TimePeriod


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
        fields = ['accepted','comment']

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
    session = forms.ModelChoiceField(
        queryset=Conference.get_sessions())

    start = forms.DateTimeField()
    end = forms.DateTimeField()

    def save(self, commit=True):
        lecture = super(LectureForm, self).save(commit=False)
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

class PublicationCreateForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = models.Publication
        fields = ['lecture', 'description']

class PublicationUpdateForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = models.Publication
        fields = ['lecture', 'description']
