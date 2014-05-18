# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets

from conferences import models


class ReviewerForm(forms.ModelForm):
    class Meta:
        model = models.Reviewer
        fields = ['user_account', 'first_name', 'last_name', 'email', 'title',
                  'contact_phone', 'availability']


class SessionForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128,
        help_text="Please enter the session name")
    duration = forms.ModelChoiceField(
        queryset=models.TimePeriod.objects.all(),
        help_text="Please choose duration of session")
    conference = forms.ModelChoiceField(
        queryset=models.Conference.objects.all(),
        help_text="Please choose conference")
    topic = forms.ModelChoiceField(
        queryset=models.Topic.objects.all(),
        help_text="Please choose session topic")
    admins = forms.ModelMultipleChoiceField(
        queryset=models.User.objects.all())
    admins.help_text = 'Please choose Admin'

    class Meta:
        model = models.Session


class TimePeriodForm(forms.ModelForm):
    description = forms.CharField(
        max_length=128,
        help_text="Please enter the description of the Time Period")
    start = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    end = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    class Meta:
        model = models.TimePeriod

    def __init__(self, *args, **kwargs):
        super(TimePeriodForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = widgets.AdminSplitDateTime()
        self.fields['end'].widget = widgets.AdminSplitDateTime()


class LectureForm(forms.ModelForm):
    class Meta:
        model = models.Lecture
        fields = ['session', 'referents', 'summary', 'duration']


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