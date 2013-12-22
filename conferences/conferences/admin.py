from django.contrib.admin.sites import AlreadyRegistered
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.db.models import get_models, get_app

# Register your models here.

def autoregister(*app_list):
    for app_name in app_list:
        app_models = get_app(app_name)
        for model in get_models(app_models):
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass


autoregister('conferences')
