from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
import traceback
from datetime import datetime


from filer.fields.file import FilerFileField
from conferences.models import Reviewer, Session, Lecture, UserProfile, Review, Conference, TimePeriod, Topic, Summary, ConferencesFile

class Command(BaseCommand):
    args = ''
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            #usuwanie danych
            Site.objects.all().delete()
            TimePeriod.objects.all().delete()
            Conference.objects.all().delete()
            Group.objects.all().delete()
            ConferencesFile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            #odcinki czasu
            tp=TimePeriod(start=datetime.strptime('2014-06-28', '%Y-%m-%d'),end=datetime.strptime('2014-09-28', '%Y-%m-%d'))
            tp.save()
            #site
            site=Site.objects.create(pk=1, domain='mdev.5buckchuck.com', name='5buckchuck.com')
            #konferencje
            c=Conference(name='konferencja',duration=tp,summaries_submission_period=tp,publications_submission_period=tp,site=site)
            # c.registration_periods.add(tp)
            c.save()

            #administratorzy
            u=User(username="administrator",password="admin",email="administrator@poczta.pl")
            u.save()


            #tematy
            t=Topic(conference=c,name="Temat 1")
            t.save()
            t2=Topic(conference=c,name="Temat 2",super_topic=t)
            t2.save()

            #administratorzy sesji
            g=Group(name="administatorzy sesji")
            g.save()
            u=User(username="administrator_sesji",password="admin",email="administratorSesji@poczta.pl")
            u.save()
            u.groups.add(g)

            #referujacy
            g=Group(name="referujacy")
            g.save()
            u=User(username="referujacy1",password="admin",email="referujacy1@poczta.pl")
            u.save()
            u.groups.add(g)
            u=User(username="referujacy2",password="admin",email="referujacy2@poczta.pl")
            u.save()
            u.groups.add(g)

            #sesje
            s=Session()
            s.conference=c
            s.topic=t
            s.name="Sesja 1"
            s.duration=tp
            s.save()
            s.admins.add(u)
            s.save()

            #plik
            #cf = ConferencesFile()
            #cf.author=User.objects.get(username="referujacy1")
            #cf.status='OK'
            #cf.filer=FilerFileField()
            #cf.save()

            #podsumowanie
            #summary=cf
            #summary.conference=c
            #summary.save()

            #wyklady
            #l=Lecture(session=s,summary=summary,duration=tp)
            #l.save()
            #l.referetns.add(User.objects.get(username='referujacy1'))

        except Exception,args:
            self.stdout.write('Cos poszlo nie tak %s ' % traceback.format_exc())