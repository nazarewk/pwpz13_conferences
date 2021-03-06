# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta
from django import forms
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core import mail
from django.db.models import Q
from django.forms import widgets
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.timezone import utc
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.datetime_safe import datetime

from .forms import (ReviewerForm, SessionForm, TimePeriodForm, LectureForm, UserForm, SummaryForm,
                    PublicationCreateForm,
                    PublicationUpdateForm, ReviewCreateForm, TopicForm,
                    ReviewUpdateForm, SendingEmailForm, SummaryUpdateForm, SendingEmailsForm, FilterForm, AccountForm,
                    ConferenceRegistrationForm, PaymentsConfirmFormSet, PaymentConfirmForm)
from .models import (Reviewer, Session, Lecture, UserProfile, Review, ConferencesFile, Summary, Publication, Topic,
                     Balance,
                     Conference, Price, Payment, TimePeriod)


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
        reviewer = Reviewer.objects.filter(user_account=user)
        publications = Review.objects.filter(reviewer=reviewer, editable=True, file_reviewed__publication__isnull=False)
        summaries = Review.objects.filter(reviewer=reviewer, editable=True, file_reviewed__summary__isnull=False)
        return render(request, "conferences/reviews/reviews_list.html", {
            'publication_reviews': publications,
            'summary_reviews': summaries
        })
    else:
        text = _('Musisz być zalogowany jako recenzent żeby mieć dostęp do tej sekcji.')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)


def review_add(request, file_id=None):
    if request.method == 'POST':
        form = ReviewCreateForm(data=request.POST)
        if form.is_valid():
            review = Review.objects.create(
                reviewer_id=request.POST['reviewer'],
                file_reviewed_id=request.POST['file_reviewed'])
            review.save()
            return render(request, 'conferences/base.html', {
                'content': _('Dodano recencje %(review)s') % {
                    'review': review.file_reviewed.name
                }
            })
    else:
        review = Review()
        try:
            review.file_reviewed_id = file_id
        except:
            pass
        form = ReviewCreateForm(instance=review)
    return render(request, "conferences/reviews/review_add.html",
                  {'form': form})


def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewUpdateForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect('review-list')
        else:
            print form.errors
    else:
        form = ReviewUpdateForm(instance=review)

    return render(request, 'conferences/reviews/review_edit.html',
                  {'form': form})

def review_delete(request,pk):
    review=get_object_or_404(Review, pk=pk)
    review.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def topic_details(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "conferences/topics/topic.html",
                  {'topic': topic})


def topic_list(request):
    user = request.user
    if user.is_authenticated():
        topics = Topic.objects.all()

        return render(request, 'conferences/topics/topic_list.html',
                      {'topics': topics})
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
            return redirect('topic-details', pk)
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

            return redirect('session-list')
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

            return redirect('session-list')
        else:
            print form.errors
    else:
        form = SessionForm(instance=session)

    return render(request, 'conferences/sessions/edit_session.html',
                  {'form': form})


def session_delete(request, pk):
    context_dict = {}
    session = get_object_or_404(Session, pk=pk)
    context_dict['session_name'] = session.name
    session.delete()

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
        lectures_list = Lecture.objects.all().order_by('duration__end')
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

            return redirect('lecture-list')
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

            return redirect('lecture-list')
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

    return render(request, "conferences/users/login.html")


def registration(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()
            activation_url = request.build_absolute_uri(reverse('user-confirm', kwargs={
                'key': user.userprofile.activation_key
            }))
            balance = user.balance
            balance.is_student = request.POST.get('student', False)
            balance.save()
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
                    conference=Conference.get_current(),
                    owner=request.user,
                    original_filename=f.name,
                    description=request.POST['description'],
                    file=file_data)
                summary.save()
                return render(request, 'conferences/base.html', {
                    'content': _('Dodano streszczenie <a href="%(summary)s">%(summary)s</a>,') % {
                        'summary': summary.url
                    }
                })
            else:
                print summary_form.errors
        else:
            summary_form = SummaryForm()
            if not Conference.get_current().is_admin(user):
                summary_form.fields['owner'].widget = widgets.HiddenInput()
        return render(
            request,
            'conferences/summary/add_summary.html',
            {'form': summary_form})
    else:
        text = _('Musisz być zalogowany, aby przesłać streszczenie')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)


def summary_details(request, pk):
    summary = get_object_or_404(Summary, pk=pk)
    return render(request, "conferences/summary/summary_details.html",
                  {'summary': summary})


def summary_edit(request, pk):
    summary = get_object_or_404(Summary, pk=pk)
    if request.method == 'POST':
        form = SummaryUpdateForm(request.POST, instance=summary)

        if form.is_valid():
            form.save()

            return redirect('summary-list')
    else:
        form = SummaryUpdateForm(instance=summary)
        reviews = []
        for r in summary.review_set.all():
            reviews.append(r)
        if not Conference.get_current().is_admin(request.user):
            form.fields['owner'].widget = widgets.HiddenInput()
    return render(request, 'conferences/summary/summary_edit.html',
                  {'summary': summary,'reviews':reviews, 'form': form})

def summary_list(request):
    user = request.user
    if Conference.is_admin(user):
        if request.GET.get('filter'):
            filter = request.GET.get('filter')
            if filter == 'accepted':
                summaries = Summary.objects.filter(status='OK')
            if filter == 'ready':
                summaries = Summary.objects.filter(status='RD')
            elif filter == 'waiting':
                summaries = Summary.objects.filter(status='PR')
            elif filter == 'rejected':
                summaries = Summary.objects.filter(status='NO')
            elif filter == 'questionable':
                summaries = Summary.objects.filter(status='IQ')
        else:
            summaries = Summary.objects.all()
        for s in summaries:
            s.reviewers =[]
            s.reviewers_accepted = []
            s.reviewers_rejected = []
            for r in s.review_set.all():
                s.reviewers.append(r.reviewer)
            for r in s.review_set.filter(status='OK'):
                s.reviewers_accepted.append(r.reviewer)
            for r in s.review_set.filter(status='RE'):
                s.reviewers_rejected.append(r.reviewer)
        filter_form = FilterForm(request.GET)
        return render(request, 'conferences/summary/summary_list.html',
                      {'summaries': summaries, 'filter_form': filter_form})
    else:
        text = _('Musisz być zalogowany, aby przesłać streszczenie.')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)


def publication_add(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            publication_form = PublicationCreateForm(request.POST, request.FILES)
            if publication_form.is_valid():
                conference = publication_form.cleaned_data['lecture'].session.conference
                start = conference.publications_submission_period.start.replace(tzinfo=None)
                end = conference.publications_submission_period.end.replace(tzinfo=None)
                if start <= datetime.now() <= end:
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
                        'content': _('Dodano publikację <a href="%(publication)s">%(publication)s</a>') % {
                            'publication': publication.url
                        }
                    })
                else:
                    text = _('Minął czas przesyłania publikacji.')
                    context = {'message': text}
                    return render(request, 'conferences/misc/no_rights.html', context)
            else:
                print publication_form.errors
        else:
            publication_form = PublicationCreateForm()
        return render(
            request,
            'conferences/publications/add_publication.html',
            {'form': publication_form})
    else:
        text = _('Musisz być zalogowany, aby przesłać publikację.')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)


def publication_edit(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = PublicationUpdateForm(request.POST, instance=publication)

        if form.is_valid():
            form.save()

            return redirect('publication-list')
        else:
            print form.errors
    else:
        form = PublicationUpdateForm(instance=publication)
        reviews = []
        for r in publication.review_set.all():
            reviews.append(r)
    return render(request, 'conferences/publications/publication_edit.html',
                  {'publication': publication,'reviews':reviews, 'form': form})


def publication_list(request):
    user = request.user
    if Conference.is_admin(user):
        if request.GET.get('filter'):
            filter = request.GET.get('filter')
            if filter == 'accepted':
                publications = Publication.objects.filter(status='OK')
            if filter == 'ready':
                publications = Publication.objects.filter(status='RD')
            elif filter == 'waiting':
                publications = Publication.objects.filter(status='PR')
            elif filter == 'rejected':
                publications = Publication.objects.filter(status='NO')
            elif filter == 'questionable':
                publications = Publication.objects.filter(status='IQ')
        else:
            publications = Publication.objects.all()
        for p in publications:
            p.reviewers =[]
            p.reviewers_accepted = []
            p.reviewers_rejected = []
            for r in p.review_set.all():
                p.reviewers.append(r.reviewer)
            for r in p.review_set.filter(status='OK'):
                p.reviewers_accepted.append(r.reviewer)
            for r in p.review_set.filter(status='RE'):
                p.reviewers_rejected.append(r.reviewer)
        filter_form = FilterForm(request.GET)
        return render(request, 'conferences/publications/publication_list.html',
                      {'publications': publications, 'filter_form': filter_form})
    else:
        text = _('Musisz być zalogowany, aby przesłać publikacje')
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


def email_send(request):
    if request.method == 'POST':
        form = SendingEmailForm(data=request.POST)
        if form.is_valid():
            user_id = request.POST['user']
            subject = request.POST['subject']
            message = request.POST['message']
            user = User.objects.get(id=user_id)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            text = _("Wysłano wiadmość.")
            context = {'message': text, 'form': form}
            return render(request, 'conferences/users/send-email.html', context)
        else:
            print form.errors
            context = {'form': form}
    else:
        form = SendingEmailForm()
        context = {'form': form}
    return render(request, 'conferences/users/send-email.html', context)


def multi_email_send(request):
    if request.method == 'POST':
        form = SendingEmailsForm(data=request.POST)
        if form.is_valid():
            subject = request.POST['subject']
            message = request.POST['message']
            groups = form.cleaned_data.get('group')
            connection = mail.get_connection()
            connection.open()
            if 'users' in groups:
                users = User.objects.all()
                for u in users:
                    email = mail.EmailMessage(subject, message, settings.EMAIL_HOST_USER,
                                              [u.email], connection=connection)
                    email.send()
                text = _("Wysłano masową wiadomość.")
                context = {'message': text, 'form': form}
                return render(request, 'conferences/users/send-email.html', context)

            if 'reviewers' in groups:
                reviewers = Reviewer.objects.all()
                for r in reviewers:
                    email = mail.EmailMessage(subject, message, settings.EMAIL_HOST_USER,
                                              [r.user_account.email], connection=connection)
                    email.send()

            sessions = Session.objects.all()
            for s in sessions:
                if s.name in groups:
                    admins = s.admins.all()
                    for a in admins:
                        email = mail.EmailMessage(subject, message, settings.EMAIL_HOST_USER,
                                                  [a.email], connection=connection)
                        email.send()
            connection.close()
            text = _("Wysłano masową wiadomość.")
            context = {'message': text, 'form': form}
            return render(request, 'conferences/users/send-email.html', context)
        else:
            print form.errors
            context = {'form': form}
    else:
        form = SendingEmailsForm()
        context = {'form': form}
    return render(request, 'conferences/users/send-email.html', context)


def payments_list(request):
    context_dict = {}
    users = []
    for u in User.objects.all():
        if u.balance.payments.count():
            users.append(u)
    context_dict['users'] = users
    return render(request, 'conferences/payments/payment_list.html', context_dict)


def account(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            account_form = AccountForm(request.user, data=request.POST)
            if account_form.is_valid():
                new_pass = request.POST['new_password']
                user.set_password(new_pass)
                user.save()
                text = _('Zmieniono hasło.')
                account_form = AccountForm(request.user)
                context = {
                    'message': text,
                    'form': account_form,
                    'user': user
                }
            else:
                print account_form.errors
                context = {'form': account_form}
        else:
            account_form = AccountForm(request.user)
            context = {'form': account_form}
        return render(request, 'conferences/users/account.html', context)
    else:
        text = _('Musisz być zalogowany, aby przesłać publikację.')
        context = {'message': text}
        return render(request, 'conferences/misc/no_rights.html', context)


@login_required
def conference_registration(request):
    if request.method == 'GET' and request.GET:
        form = ConferenceRegistrationForm(request.GET)
        if form.is_valid():
            balance = request.user.balance
            now = datetime.utcnow().replace(tzinfo=utc)
            pay_until = now + timedelta(days=7)
            ids = []
            prefix = ConferenceRegistrationForm.prefix
            for name, count in form.cleaned_data.items():
                if count and name.startswith(prefix):
                    price_id = int(name[len(prefix):])
                    price = get_object_or_404(Price, id=price_id)
                    for i in range(count):
                        tp = TimePeriod(start=now, end=pay_until)
                        tp.save()
                        p = Payment(
                            balance=balance,
                            short_description=price.title,
                            time_to_pay=tp,
                            amount=price.value
                        )
                        p.save()
                        ids.append(p.id)
            formset = PaymentsConfirmFormSet(
                queryset=Payment.objects.filter(id__in=ids))
            for f in formset:
                f.fields['summary'].queryset = Summary.objects.filter(payment__isnull=True, owner=request.user)
            return render(request, 'conferences/conference/register_confirm.html', {
                'formset': formset
            })
        return render(request, 'conferences/conference/register.html', {
            'form': form
        })
    elif request.method == 'POST':
        formset = PaymentsConfirmFormSet(request.POST)
        for f in formset:
            f.fields['summary'].queryset = Summary.objects.filter(payment__isnull=True, owner=request.user)
        if formset.is_valid():
            formset.save()
            return redirect('account')
        return render(request, 'conferences/conference/register_confirm.html', {
            'formset': formset
        })
    else:
        form = ConferenceRegistrationForm()
        return render(request, 'conferences/conference/register.html', {
            'form': form
        })


@login_required
def payment_confirm(request, pk):
    payment = request.user.balance.payments.get(id=pk)
    if not payment:
        return render(request, 'conferences/base.html', {
            'content': _('Nie znaleziono płatności') % (payment,)
        })
    if request.method == 'POST':
        form = PaymentConfirmForm(data=request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = PaymentConfirmForm(instance=payment)
        form.fields['summary'].queryset = Summary.objects.filter(payment__isnull=True, owner=request.user)
    return render(request, 'conferences/payments/payment_user_edit.html', {
        'form': form
    })


@login_required
def payment_delete(request, pk):
    payment = request.user.balance.payments.get(id=pk)
    if not payment:
        return render(request, 'conferences/base.html', {
            'content': _('Nie znaleziono płatności') % (payment,)
        })
    payment.delete()
    return redirect('account')


@login_required
def payments_pay(request, pk):
    balance = request.user.balance
    payment = request.user.balance.payments.get(id=pk)
    if balance.set_paid(payment):
        return redirect('account')
    return render(request, 'conferences/base.html', {
        'content': _('Nie udało się zapłacić za %s') % (payment,)
    })
