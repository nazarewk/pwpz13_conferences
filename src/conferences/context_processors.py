from .models import Conference


def is_conference_admin(request):
    c = Conference.get_current()
    return {
        'IS_CONFERENCE_ADMIN': c.is_admin(request.user) if c else False
    }