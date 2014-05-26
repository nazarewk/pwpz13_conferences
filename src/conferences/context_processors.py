from .models import Conference


def is_conference_admin(request):
    return {
        'IS_CONFERENCE_ADMIN': Conference.get_current().is_admin(request.user)
    }