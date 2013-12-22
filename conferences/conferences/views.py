from django.utils.translation import ugettext as _
from django.shortcuts import render

# Create your views here.

# testView

from django.shortcuts import render_to_response

def home(request):
    return render_to_response("home.html", {'data': "Hello there!"})