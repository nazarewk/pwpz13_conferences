# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import ReviewerForm, SessionForm, TimePeriodForm, LectureForm, UserForm
from .models import Reviewer, Session, Lecture, UserProfile, User, Site
import hashlib, string, random


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
            #form.save()
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


def session_details(request, pk):
    context_dict = {}

    try:
        session = Session.objects.get(pk=pk)
        lectures = Lecture.objects.filter(session=session)
        context_dict['session'] = session
        context_dict['lectures'] = lectures
    except Session.DoesNotExist:
        pass

    return render_to_response('conferences/sessions/session.html',
                              context_dict)


def session_list(request):
    context_dict = {}
    sessions_list = Session.objects.all()
    context_dict['sessions'] = sessions_list

    return render_to_response('conferences/sessions/session_list.html',
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

    return render_to_response('conferences/sessions/add_session.html',
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

    return render_to_response('conferences/sessions/edit_session.html',
                              {'form': form})


def session_delete(request, pk):
    context_dict = {}
    session = get_object_or_404(Session, pk=pk)
    context_dict['session'] = session
    session_del = session.delete()
    context_dict['sessions_del'] = session_del

    return render_to_response('conferences/sessions/remove_session.html',
                              context_dict)


def timeperiod_add(request):
    if request.method == 'POST':
        form = TimePeriodForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

        else:
            # TODO: Tu chyba cos powinno byc??
            form.errors

    else:
        form = TimePeriodForm()

    return render_to_response('conferences/misc/add_timeperiod.html',
                              {'form': form})


def lecture_details(request, pk):
    context_dict = {}

    try:
        lecture = get_object_or_404(Lecture, pk=pk)
        context_dict['lecture'] = lecture
    except Session.DoesNotExist:
        pass

    return render_to_response('conferences/lectures/lecture.html',
                              context_dict)


def lecture_list(request):
    context_dict = {}
    lectures_list = Lecture.objects.all()
    context_dict['lectures'] = lectures_list

    return render_to_response('conferences/lectures/lecture_list.html',
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

    return render_to_response('conferences/lectures/add_lecture.html',
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

    return render_to_response('conferences/lectures/edit_lecture.html',
                              {'form': form})


def lecture_delete(request, pk):
    context_dict = {}
    lecture = get_object_or_404(Lecture, pk=pk)
    context_dict['lecture'] = lecture
    lecture_del = lecture.delete()
    context_dict['lecture_del'] = lecture_del

    return render_to_response('conferences/lectures/lecture_delete.html',
                              context_dict)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                text = u"Użytkownik nie został aktywowany. Sprawdź pocztę, a następnie kliknij w link z aktywacją."
                context = {'message': text}
                return render(request, 'conferences/users/login.html', context)
        else:
            text = u"Nazwa użytkownika lub hasło jest niepoprawne."
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
            activation_key = hashlib.md5(user.username).hexdigest()
            activation_key += ''.join(random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits)
                                      for i in range(8))
            profile = UserProfile.create(user, activation_key)
            current_site = Site.objects.get_current()
            site_url = current_site.domain + "/users/confirm/" + user.username + "/" + activation_key
            title = u"Potwierdzenie rejestracji"
            content = u"Aby dokończyć rejestrację kliknij w link aktywacyjny " + site_url
            # Nie wiem jak wysłać maila, czy to poleci na podstawie ustawien z django, czy mailem admina, czy jeszcze jak
            # dlatego send_mail zakomentowane, trzeba poprawic adres a reszta powinna byc ok
            # send_mail(title, content, jakis_adres, [user.email], fail_silently=False)
            profile.save()
            text = u"Na podany adres został wysłany link aktywacyjny."
            context = {'message': text}
            return render(request, 'conferences/users/confirm.html', context)
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render(request, "conferences/users/registration.html",
                  {'form': user_form})


@login_required
def user_logout(request):
    logout(request)
    return render(request, "conferences/home.html")


def user_confirm(request, username, key):
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        if profile.activation_key == key:
            user.is_active = True
            user.save()
            profile.save()
            text = u"Konto aktywowane. Teraz możesz się zalogować."
            context = {'message': text}
            return render(request, 'conferences/users/confirm.html', context)
        else:
            text = u'Niepoprawny klucz aktywacyjny.'
            context = {'message': text}
            return render(request, 'conferences/users/confirm.html', context)
    except (User.DoesNotExist, UserProfile.DoesNotExist) as e:
        text = u'Niepoprawny klucz aktywacyjny.'
        context = {'message': text}
        return render(request, 'conferences/users/confirm.html', context)

