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

from .models import ReviewerForm, SessionForm
from .models import Reviewer, Session


def home(request):
    return render_to_response("conferences/home.html", {'data': "Hello there!"})

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
        form=ReviewerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/reviewers/')
    else:
        form = ReviewerForm(instance=reviewer)
    return render(request,"conferences/reviewers/reviewer_edit.html", {'form':form})

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
        context_dict['session'] = session
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
    session = Session.objects.get(pk=pk)

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
    session = Session.objects.get(pk=pk)
    context_dict['session'] = session
    session_del = session.delete()
    context_dict['sessions_del'] = session_del

    return render_to_response('conferences/sessions/remove_session.html', context_dict, context)