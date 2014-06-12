from django import template
from django.template import loader, Context
from conferences.models import Conference

register = template.Library()


@register.inclusion_tag('conferences/topics/topic_tree.html')
def render_topics(is_admin=False, topics=Conference.get_current().topics.filter(parent=None)):
    def get_ctx(topics):
        return [
            {
                'id': topic.id,
                'name': topic.name,
                'children': get_ctx(topic.children.all())
            } if topic.children else {
                'id': topic.id,
                'name': topic.name
            } for topic in topics]
    return {
        'topics': get_ctx(topics),
        'is_admin': is_admin,
    }
