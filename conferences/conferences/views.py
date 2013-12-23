from django.utils.translation import ugettext as _
from django.shortcuts import render

# Create your views here.

# testView

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Reviewer

def home(request):
    return render_to_response("conferences/home.html", {'data': "Hello there!"})

#reviewers views section
class ReviewerListView(ListView):

    model = Reviewer

    def get_context_data(self, **kwargs):
        context=super(ReviewerListView,self).get_context_data( **kwargs)
        return context


class ReviewerDetailView(DetailView):

    model = Reviewer

    def get_context_data(self, **kwargs):
        context = super(ReviewerDetailView, self).get_context_data(**kwargs)
        return context
