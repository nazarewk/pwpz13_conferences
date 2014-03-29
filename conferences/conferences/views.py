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

from .models import ReviewerForm
from .models import Reviewer

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