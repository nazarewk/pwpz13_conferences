from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ConferencesAppHook(CMSApp):
    name = _("Konferencje")
    urls = ["conferences.urls"]

apphook_pool.register(ConferencesAppHook)