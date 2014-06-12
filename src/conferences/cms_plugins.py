from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _


class TopicsPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Tematy')
    render_template = "conferences/topics/topic_tree_cms.html"


plugin_pool.register_plugin(TopicsPlugin)