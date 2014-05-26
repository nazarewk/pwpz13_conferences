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
from django.core.files.base import ContentFile
from django.conf import settings
import tempfile

from .context_processors import is_conference_admin

from .forms import ReviewerForm, SessionForm, TimePeriodForm, LectureForm, UserForm, SummaryForm, PublicationForm, ReviewForm, TopicForm
from .models import Reviewer, Session, Lecture, UserProfile, Review, ConferencesFile, Summary, Publication, Topic


def home(request):
    return render(request, "conferences/home.html")


def reviewer_list(request):
    try:
        user = request.user
        if user.is_authenticated():
            reviewers = Reviewer.objects.filter(is_active=True)
            return render(request, "conferences/reviewers/reviewer_list.html",
                          {'reviewers': reviewers})
    except:
        pass
    text = _('Musisz być zalogowany jako admin żeby mieć dostęp do tej sekcji.')
    context = {'message': text}
    return render(request, 'conferences/misc/no_rights.html', context)



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


def review_list(request):
    user = request.user
    if user.reviewer:
        reviewer=Reviewer.objects.filter(user_account=user)
        reviews = Review.objects.filter(reviewer=reviewer)
        return render(request, "conferences/reviews/reviews_list.html",
                  {'reviews': reviews})
    else:
        text = _('Musisz być zalogowany jako recenzent żeby mieć dostęp do tej sekcji.')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)

def review_add(request):
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = Review.objects.create(
                reviewer_id=request.POST['reviewer'],
                file_reviewed_id=request.POST['file_reviewed'],
                accepted=False)
            review.save()
            return render(request, 'conferences/base.html', {
                    'content': _('Dodano recencje %(review)s') % {
                        'review': review.file_reviewed.name
                    }
                })
    else:
        form = ReviewForm()
    return render(request, "conferences/reviews/review_add.html",
                  {'form': form})

def topic_details(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "conferences/topics/topic.html",
                  {'topic': topic})

def topic_list(request):
    user = request.user
    if user.is_authenticated():
        topics = Topic.objects.all()

        return render(request, 'conferences/topics/topic_list.html',
                      {'topics':topics})
    else:
        text = _('Musisz być zalogowany.')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)


def topic_add(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('topic-list')
        else:
            print form.errors
    else:
        form = TopicForm()

    return render(request, 'conferences/topics/add_topic.html',
                  {'form': form})


def topic_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)

        if form.is_valid():
            form.save(commit=True)
            return redirect('topic-details',pk)
        else:
            print form.errors
    else:
        form = TopicForm(instance=topic)

    return render(request, 'conferences/topics/edit_topic.html',
                  {'form': form})

def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.delete()
    return redirect('topic-list')

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
    user = request.user
    if user.is_authenticated():
        context_dict = {}
        sessions_list = Session.objects.all()
        context_dict['sessions'] = sessions_list

        return render(request, 'conferences/sessions/session_list.html',
                      context_dict)
    else:
        text = _('Musisz być zalogowany.')
        context = {'message': text}
        return render(request, 'conferences/sessions/session_list.html', context)


def session_add(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('pages-root')
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

            return redirect('pages-root')
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

            return redirect('pages-root')

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
    user = request.user
    if user.is_authenticated():
        context_dict = {}
        lectures_list = Lecture.objects.all()
        context_dict['lectures'] = lectures_list

        return render(request, 'conferences/lectures/lecture_list.html',
                      context_dict)
    else:
        text = _('Musisz być zalogowany.')
        context = {'message': text}
        return render(request, 'conferences/lectures/lecture_list.html', context)


def lecture_add(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('pages-root')
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

            return redirect('pages-root')
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
                return redirect('pages-root')
            else:
                text = _("Użytkownik nie został aktywowany. Sprawdź pocztę, a następnie kliknij w link z aktywacją.")
                context = {'message': text}
                return render(request, 'conferences/users/login.html', context)
        else:
            text = _("Nazwa użytkownika lub hasło jest niepoprawne.")
            context = {'message': text}
            return render(request, 'conferences/users/login.html', context)

    return render(request, 'conferences/base.html', {
        'content': _('Zaloguj się.')
    })


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
    return redirect('pages-root')


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
            summary_form = SummaryForm(request.POST, request.FILES)
            if summary_form.is_valid():
                # Handle uploaded file
                f = request.FILES['file']
                file_data = ContentFile(f.read())
                file_data.name = f.name

                summary = Summary.objects.create(
                    conference_id=request.POST['conference'],
                    owner=request.user,
                    original_filename=f.name,
                    description=request.POST['description'],
                    file=file_data)
                summary.save()
                return render(request, 'conferences/base.html', {
                    'content': _('Dodano streszczenie %(summary)s') % {
                        'summary': summary.url
                    }
                })
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
        return render(request, 'conferences/misc/no_rights.html', context)

def summary_list(request):
    user = request.user
    if is_conference_admin:
        summaries=Summary.objects.all()
        return render(request, 'conferences/summary/summary_list.html',
                      { 'summaries':summaries})
    else:
        text = _('Musisz być zalogowany, aby przesłać streszczenie')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)

def publication_add(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            publication_form = PublicationForm(request.POST, request.FILES)
            if publication_form.is_valid():
                # Handle uploaded file
                f = request.FILES['file']
                file_data = ContentFile(f.read())
                file_data.name = f.name

                publication = Publication.objects.create(
                    lecture_id=request.POST['lecture'],
                    owner=request.user,
                    original_filename=f.name,
                    description=request.POST['description'],
                    file=file_data)
                publication.save()
                return render(request, 'conferences/base.html', {
                    'content': _('Dodano publikację %(publication)s') % {
                        'publication': publication.url
                    }
                })
            else:
                print publication_form.errors
        else:
            publication_form = PublicationForm()
        return render(
            request,
            'conferences/publication/add_publication.html',
            {'form': PublicationForm})
    else:
        text = _('Musisz być zalogowany, aby przesłać streszczenie')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)


'''
    def create_file(self, folder, filename=None):
        filename = filename or 'test_file.dat'
        file_data = django.core.files.base.ContentFile('some data')
        file_data.name = filename
        file_obj = File.objects.create(owner=self.superuser, original_filename=filename, file=file_data, folder=folder)
        file_obj.save()
        return file_obj
'''
