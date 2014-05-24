# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

from .forms import ReviewerForm, SessionForm, TimePeriodForm, LectureForm, UserForm, SummaryForm
from .models import Reviewer, Session, Lecture, UserProfile, Review


def home(request):
    return render(request, "conferences/home.html")


def reviewer_list(request):
    reviewers = Reviewer.objects.filter(is_active=True)
    return render(request, "conferences/reviewers/reviewer_list.html",
                  {'reviewers': reviewers})


def reviewer_details(request, pk):
    reviewer = Reviewer.objects.get(pk=pk)
    if reviewer.user_account:
        reviewer.first_name = reviewer.user_account.first_name
        reviewer.last_name = reviewer.user_account.last_name
        reviewer.email = reviewer.user_account.email
    return render(request, "conferences/reviewers/reviewer_detail.html",
                  {'reviewer': reviewer})


def reviewer_create(request):
    if request.method == 'POST':
        form = ReviewerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviewer-list')
    else:
        form = ReviewerForm()
    return render(request, "conferences/reviewers/reviewer_create.html",
                  {'form': form})


def reviewer_edit(request, pk):
    reviewer = get_object_or_404(Reviewer, pk=pk)
    if request.method == 'POST':
        availability = request.POST.get('availability', '')
        form = ReviewerForm(request.POST, instance=reviewer)
        if form.is_valid():
            # form.save()
            reviewer.availability = availability
            reviewer.save()
            return redirect('reviewer-list')
    else:
        if (reviewer.user_account):
            reviewer.first_name = reviewer.user_account.first_name
            reviewer.last_name = reviewer.user_account.last_name
            reviewer.email = reviewer.user_account.email
        form = ReviewerForm(instance=reviewer)
    return render(request, "conferences/reviewers/reviewer_edit.html",
                  {'form': form, 'reviewer': reviewer})


def reviewer_delete(request, pk):
    reviewer = Reviewer.objects.get(pk=pk)
    reviewer.is_active = False
    reviewer.save()
    return redirect('reviewer-list')


def reviews_list(request):
    reviews = Review.objects.filter(reviewer=request.user)
    return render(request, "conferences/reviews/reviews_list.html",
                  {'reviews': reviews})


def session_details(request, pk):
    context_dict = {}

    try:
        session = Session.objects.get(pk=pk)
        lectures = Lecture.objects.filter(session=session)
        context_dict['session'] = session
        context_dict['lectures'] = lectures
    except Session.DoesNotExist:
        pass

    return render(request, 'conferences/sessions/session.html',
                  context_dict)


def session_list(request):
    context_dict = {}
    sessions_list = Session.objects.all()
    context_dict['sessions'] = sessions_list

    return render(request, 'conferences/sessions/session_list.html',
                  context_dict)


def session_add(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
        else:
            print form.errors
    else:
        form = SessionForm()

    return render(request, 'conferences/sessions/add_session.html',
                  {'form': form})


def session_edit(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)

        if form.is_valid():
            form.save(commit=True)

            return redirect('home')
        else:
            print form.errors
    else:
        form = SessionForm(instance=session)

    return render(request, 'conferences/sessions/edit_session.html',
                  {'form': form})


def session_delete(request, pk):
    context_dict = {}
    session = get_object_or_404(Session, pk=pk)
    context_dict['session'] = session
    session_del = session.delete()
    context_dict['sessions_del'] = session_del

    return render(request, 'conferences/sessions/remove_session.html',
                  context_dict)


def timeperiod_add(request):
    if request.method == 'POST':
        form = TimePeriodForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

        else:
            print form.errors

    else:
        form = TimePeriodForm()

    return render(request, 'conferences/misc/add_timeperiod.html',
                  {'form': form})


def lecture_details(request, pk):
    context_dict = {}

    try:
        lecture = get_object_or_404(Lecture, pk=pk)
        context_dict['lecture'] = lecture
    except Session.DoesNotExist:
        pass

    return render(request, 'conferences/lectures/lecture.html',
                  context_dict)


def lecture_list(request):
    context_dict = {}
    lectures_list = Lecture.objects.all()
    context_dict['lectures'] = lectures_list

    return render(request, 'conferences/lectures/lecture_list.html',
                  context_dict)


def lecture_add(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
        else:
            print form.errors
    else:
        form = LectureForm()

    return render(request, 'conferences/lectures/add_lecture.html',
                  {'form': form})


def lecture_edit(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)

    if request.method == 'POST':
        form = LectureForm(request.POST, instance=lecture)

        if form.is_valid():
            form.save(commit=True)

            return redirect('home')
        else:
            print form.errors
    else:
        form = LectureForm(instance=lecture)

    return render(request, 'conferences/lectures/edit_lecture.html',
                  {'form': form})


def lecture_delete(request, pk):
    context_dict = {}
    lecture = get_object_or_404(Lecture, pk=pk)
    context_dict['lecture'] = lecture
    lecture_del = lecture.delete()
    context_dict['lecture_del'] = lecture_del

    return render(request, 'conferences/lectures/lecture_delete.html',
                  context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                text = _("Użytkownik nie został aktywowany. Sprawdź pocztę, a następnie kliknij w link z aktywacją.")
                context = {'message': text}
                return render(request, 'conferences/users/login.html', context)
        else:
            text = _("Nazwa użytkownika lub hasło jest niepoprawne.")
            context = {'message': text}
            return render(request, 'conferences/users/login.html', context)


def registration(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()
            profile = UserProfile(user=user)
            profile.save()
            activation_url = request.build_absolute_uri(reverse('user-confirm', kwargs={
                'key': profile.activation_key
            }))
            title = _('Potwierdzenie rejestracji')
            content = _("Witaj %(name)s,\nAby dokończyć rejestrację kliknij w link aktywacyjny %(url)s.") % {
                'url': activation_url,
                'name': user.username}
            send_mail(title, content, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            text = _("Na podany adres został wysłany link aktywacyjny.")
            ctx = {
                'message': text
            }
            return render(
                request,
                'conferences/users/confirm.html',
                ctx)
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    ctx = {
        'form': user_form
    }
    return render(
        request,
        "conferences/users/registration.html",
        ctx)


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


def user_confirm(request, key):
    profile = get_object_or_404(UserProfile, activation_key=key)
    user = profile.user
    if profile.activation_key == key:
        user.is_active = True
        user.save()
        profile.activation_key = None
        profile.save()
        text = _("Konto aktywowane. Teraz możesz się zalogować.")
        context = {'message': text}
        return render(request, 'conferences/users/confirm.html', context)
    else:
        text = _('Niepoprawny klucz aktywacyjny.')
        context = {'message': text}
        return render(request, 'conferences/users/confirm.html', context)


def summary_add(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            summary_form = SummaryForm(data=request.POST)
            if summary_form.is_valid():
                return render(
                    request,
                    'conferences/summary/add_summary.html')
            else:
                print summary_form.errors
        else:
            summary_form = SummaryForm()
        return render(
            request,
            'conferences/summary/add_summary.html',
            {'form': summary_form})
    else:
        text = _('Musisz być zalogowany, aby przesłać streszczenie')
        context = {'message': text}
        return render(request, 'conferences/summary/add_summary.html', context)
