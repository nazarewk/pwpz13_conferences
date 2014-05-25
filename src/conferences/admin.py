from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from django.db.models import get_models, get_app
from filer.admin.fileadmin import FileAdmin
from .models import ConferencesFile, Summary, Publication

# Register your models here.

def autoregister(app_name, excludes=[]):
    app_models = get_app(app_name)
    for model in get_models(app_models):
        if model not in excludes:
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass


excludes = [ConferencesFile, Summary, Publication]
autoregister('conferences', excludes)

for model in excludes:
    admin.site.register(model, FileAdmin)