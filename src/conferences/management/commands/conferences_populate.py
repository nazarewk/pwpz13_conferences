from django.core.management.base import BaseCommand, CommandError
from conferences.models import Conference

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print('Komenda dziala...')