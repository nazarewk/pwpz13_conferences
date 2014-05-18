# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import render

# Create your views here.

# testView

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from .models import ReviewerForm, SessionForm, TimePeriodForm, LectureForm, UserForm
from .models import Reviewer, Session, TimePeriod, Lecture, UserProfile, User, Site
import hashlib, string, random


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return render(request, "conferences/home.html")
            else:
                # tu gdy zablokowany
                return render(request, "conferences/home.html")
        else:
            # tu gdy nie ma uzytkownika
            return render(request, "conferences/home.html")
    else:
        return render(request, "conferences/home.html")

#reviewers views section

def reviewer_list(request):
    reviewers=Reviewer.objects.filter(is_active = True)
    return render(request,"conferences/reviewers/reviewer_list.html",{'reviewers':reviewers})

def reviewer_detail(request,pk):
    reviewer=Reviewer.objects.get(pk=pk)
    if(reviewer.user_account):
        reviewer.first_name=reviewer.user_account.first_name
        reviewer.last_name=reviewer.user_account.last_name
        reviewer.email=reviewer.user_account.email
    return render(request,"conferences/reviewers/reviewer_detail.html", {'reviewer':reviewer})

def reviewer_create(request):
    if request.method=='POST':
        form=ReviewerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/reviewers/')
    else:
        form = ReviewerForm()
    return render(request,"conferences/reviewers/reviewer_create.html", {'form':form})

def reviewer_edit(request,pk):
    reviewer = get_object_or_404(Reviewer,pk=pk)
    if request.method=='POST':
		availability = request.POST.get('availability','')
		form=ReviewerForm(request.POST, instance=reviewer)
		if form.is_valid():
			#form.save()
			reviewer.availability=availability
			reviewer.save()
			return redirect('/reviewers/')
    else:
		if(reviewer.user_account):
			reviewer.first_name=reviewer.user_account.first_name
			reviewer.last_name=reviewer.user_account.last_name
			reviewer.email=reviewer.user_account.email
		form = ReviewerForm(instance=reviewer)
    return render(request,"conferences/reviewers/reviewer_edit.html", {'form':form, 'reviewer':reviewer})

def RetireReviewer(request,pk):
    reviewer=Reviewer.objects.get(pk=pk)
    reviewer.is_active=False;
    reviewer.save()
    return redirect("/reviewers/")


def session(request, pk):

    context = RequestContext(request)
    context_dict = {}

    try:
        session = Session.objects.get(pk=pk)
        lectures = Lecture.objects.filter(session=session)
        context_dict['session'] = session
        context_dict['lectures'] = lectures
    except Session.DoesNotExist:
        pass

    return render_to_response('conferences/sessions/session.html', context_dict, context)


def session_list(request):

    context = RequestContext(request)
    context_dict = {}
    sessions_list = Session.objects.all()
    context_dict['sessions'] = sessions_list

    return render_to_response('conferences/sessions/session_list.html', context_dict, context)


def add_session(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            form.save()

            return home(request)
        else:
            print form.errors
    else:
        form = SessionForm()

    return render_to_response('conferences/sessions/add_session.html', {'form': form}, context)


def edit_session(request, pk):

    context = RequestContext(request)
    session = get_object_or_404(Session, pk=pk)

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)

        if form.is_valid():
            form.save(commit=True)

            return home(request)
        else:
            print form.errors
    else:
        form = SessionForm(instance=session)

    return render_to_response('conferences/sessions/edit_session.html', {'form': form}, context)


def remove_session(request, pk):

    context = RequestContext(request)
    context_dict = {}
    session = get_object_or_404(Session, pk=pk)
    context_dict['session'] = session
    session_del = session.delete()
    context_dict['sessions_del'] = session_del

    return render_to_response('conferences/sessions/remove_session.html', context_dict, context)


def add_timeperiod(request):

    context = RequestContext(request)

    if request.method =='POST':
        form = TimePeriodForm(request.POST)

        if form.is_valid():
            form.save()

            return home(request)

        else:
            form.errors

    else:
        form = TimePeriodForm()

    return render_to_response('conferences/misc/add_timeperiod.html', { 'form':form }, context)


def lecture(request, pk):
    context = RequestContext(request)
    context_dict = {}

    try:
        lecture = get_object_or_404(Lecture,pk=pk)
        context_dict['lecture'] = lecture
    except Session.DoesNotExist:
        pass

    return render_to_response('conferences/lectures/lecture.html', context_dict, context)


def lecture_list(request):

    context = RequestContext(request)
    context_dict = {}
    lectures_list = Lecture.objects.all()
    context_dict['lectures'] = lectures_list

    return render_to_response('conferences/lectures/lecture_list.html', context_dict, context)


def add_lecture(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = LectureForm(request.POST)

        if form.is_valid():
            form.save()

            return home(request)
        else:
            print form.errors
    else:
        form = LectureForm()

    return render_to_response('conferences/lectures/add_lecture.html', {'form': form}, context)


def edit_lecture(request, pk):

    context = RequestContext(request)
    lecture = get_object_or_404(Lecture,pk=pk)

    if request.method == 'POST':
        form = LectureForm(request.POST, instance=lecture)

        if form.is_valid():
            form.save(commit=True)

            return home(request)
        else:
            print form.errors
    else:
        form = LectureForm(instance=lecture)

    return render_to_response('conferences/lectures/edit_lecture.html', {'form': form}, context)


def remove_lecture(request, pk):

    context = RequestContext(request)
    context_dict = {}
    lecture = get_object_or_404(Lecture, pk=pk)
    context_dict['lecture'] = lecture
    lecture_del = lecture.delete()
    context_dict['lecture_del'] = lecture_del

    return render_to_response('conferences/lectures/remove_lecture.html', context_dict, context)

def registration(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()
            activation_key = hashlib.md5(user.username).hexdigest()
            activation_key += ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(8))
            profile = UserProfile.create(user, activation_key)
            current_site = Site.objects.get_current()
            site_url = current_site.domain + "/users/confirm/" + user.username + "/" + activation_key
            title = "Potwierdzenie rejestracji"
            content = "Aby dokończyć rejestrację kliknij w link aktywacyjny " + site_url
            # Nie wiem jak wysłać maila, czy to poleci na podstawie ustawien z django, czy mailem admina, czy jeszcze jak
            # dlatego send_mail zakomentowane, trzeba poprawic adres a reszta powinna byc ok
	        # send_mail(title, content, jakis_adres, [user.email], fail_silently=False)
            profile.save()
            return redirect('/')
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render(request, "conferences/users/registration.html", {'form': user_form})


@login_required
def user_logout(request):
    logout(request)
    return render(request, "conferences/home.html")


def user_confirm(request, username, key):
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        if profile.activation_key==key:
            user.is_active = True
            user.save()
            profile.save()
            text = "Konto aktywowane. Teraz możesz się zalogować."
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