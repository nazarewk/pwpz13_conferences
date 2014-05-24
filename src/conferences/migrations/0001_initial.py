# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TimePeriod'
        db.create_table(u'conferences_timeperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'conferences', ['TimePeriod'])

        # Adding model 'Conference'
        db.create_table(u'conferences_conference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('duration', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'conference_durations', to=orm['conferences.TimePeriod'])),
            ('summaries_submission_period', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'summaries_submissions', to=orm['conferences.TimePeriod'])),
            ('publications_submission_period', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'publications_submissions', to=orm['conferences.TimePeriod'])),
        ))
        db.send_create_signal(u'conferences', ['Conference'])

        # Adding M2M table for field admins on 'Conference'
        m2m_table_name = db.shorten_name(u'conferences_conference_admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conference', models.ForeignKey(orm[u'conferences.conference'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conference_id', 'user_id'])

        # Adding M2M table for field registration_periods on 'Conference'
        m2m_table_name = db.shorten_name(u'conferences_conference_registration_periods')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conference', models.ForeignKey(orm[u'conferences.conference'], null=False)),
            ('timeperiod', models.ForeignKey(orm[u'conferences.timeperiod'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conference_id', 'timeperiod_id'])

        # Adding model 'ConferencesFile'
        db.create_table(u'conferences_conferencesfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filer.File'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'conferences', ['ConferencesFile'])

        # Adding model 'Summary'
        db.create_table(u'conferences_summary', (
            (u'conferencesfile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conferences.ConferencesFile'], unique=True, primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'summaries', to=orm['conferences.Conference'])),
        ))
        db.send_create_signal(u'conferences', ['Summary'])

        # Adding model 'Publication'
        db.create_table(u'conferences_publication', (
            (u'conferencesfile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conferences.ConferencesFile'], unique=True, primary_key=True)),
            ('lecture', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'publications', to=orm['conferences.Lecture'])),
        ))
        db.send_create_signal(u'conferences', ['Publication'])

        # Adding model 'Reviewer'
        db.create_table(u'conferences_reviewer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True, blank=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'conferences', ['Reviewer'])

        # Adding M2M table for field availability on 'Reviewer'
        m2m_table_name = db.shorten_name(u'conferences_reviewer_availability')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reviewer', models.ForeignKey(orm[u'conferences.reviewer'], null=False)),
            ('timeperiod', models.ForeignKey(orm[u'conferences.timeperiod'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reviewer_id', 'timeperiod_id'])

        # Adding M2M table for field unavailability on 'Reviewer'
        m2m_table_name = db.shorten_name(u'conferences_reviewer_unavailability')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reviewer', models.ForeignKey(orm[u'conferences.reviewer'], null=False)),
            ('timeperiod', models.ForeignKey(orm[u'conferences.timeperiod'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reviewer_id', 'timeperiod_id'])

        # Adding model 'Review'
        db.create_table(u'conferences_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conferences.Reviewer'])),
            ('file_reviewed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conferences.ConferencesFile'])),
            ('unguessable_id', self.gf('django.db.models.fields.CharField')(default=u'vBoVMnteOUb1KXMVBtZ9cU8FVU1lldOJ', unique=True, max_length=32)),
            ('accepted', self.gf('django.db.models.fields.BooleanField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'conferences', ['Review'])

        # Adding model 'Topic'
        db.create_table(u'conferences_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conferences.Conference'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('super_topic', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'sub_topics', null=True, to=orm['conferences.Topic'])),
        ))
        db.send_create_signal(u'conferences', ['Topic'])

        # Adding model 'Session'
        db.create_table(u'conferences_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'sessions', to=orm['conferences.Conference'])),
            ('topic', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conferences.Topic'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('duration', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'sessions_dates', to=orm['conferences.TimePeriod'])),
        ))
        db.send_create_signal(u'conferences', ['Session'])

        # Adding M2M table for field admins on 'Session'
        m2m_table_name = db.shorten_name(u'conferences_session_admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm[u'conferences.session'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['session_id', 'user_id'])

        # Adding model 'Lecture'
        db.create_table(u'conferences_lecture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'lectures', to=orm['conferences.Session'])),
            ('summary', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conferences.Summary'], unique=True)),
            ('duration', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'lectures_dates', to=orm['conferences.TimePeriod'])),
        ))
        db.send_create_signal(u'conferences', ['Lecture'])

        # Adding M2M table for field referents on 'Lecture'
        m2m_table_name = db.shorten_name(u'conferences_lecture_referents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lecture', models.ForeignKey(orm[u'conferences.lecture'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['lecture_id', 'user_id'])

        # Adding model 'Balance'
        db.create_table(u'conferences_balance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_student', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'conferences', ['Balance'])

        # Adding model 'Payment'
        db.create_table(u'conferences_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('balance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conferences.Balance'])),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('full_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('time_to_pay', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'payments', to=orm['conferences.TimePeriod'])),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
        ))
        db.send_create_signal(u'conferences', ['Payment'])

        # Adding model 'UserProfile'
        db.create_table(u'conferences_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, blank=True)),
        ))
        db.send_create_signal(u'conferences', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'TimePeriod'
        db.delete_table(u'conferences_timeperiod')

        # Deleting model 'Conference'
        db.delete_table(u'conferences_conference')

        # Removing M2M table for field admins on 'Conference'
        db.delete_table(db.shorten_name(u'conferences_conference_admins'))

        # Removing M2M table for field registration_periods on 'Conference'
        db.delete_table(db.shorten_name(u'conferences_conference_registration_periods'))

        # Deleting model 'ConferencesFile'
        db.delete_table(u'conferences_conferencesfile')

        # Deleting model 'Summary'
        db.delete_table(u'conferences_summary')

        # Deleting model 'Publication'
        db.delete_table(u'conferences_publication')

        # Deleting model 'Reviewer'
        db.delete_table(u'conferences_reviewer')

        # Removing M2M table for field availability on 'Reviewer'
        db.delete_table(db.shorten_name(u'conferences_reviewer_availability'))

        # Removing M2M table for field unavailability on 'Reviewer'
        db.delete_table(db.shorten_name(u'conferences_reviewer_unavailability'))

        # Deleting model 'Review'
        db.delete_table(u'conferences_review')

        # Deleting model 'Topic'
        db.delete_table(u'conferences_topic')

        # Deleting model 'Session'
        db.delete_table(u'conferences_session')

        # Removing M2M table for field admins on 'Session'
        db.delete_table(db.shorten_name(u'conferences_session_admins'))

        # Deleting model 'Lecture'
        db.delete_table(u'conferences_lecture')

        # Removing M2M table for field referents on 'Lecture'
        db.delete_table(db.shorten_name(u'conferences_lecture_referents'))

        # Deleting model 'Balance'
        db.delete_table(u'conferences_balance')

        # Deleting model 'Payment'
        db.delete_table(u'conferences_payment')

        # Deleting model 'UserProfile'
        db.delete_table(u'conferences_userprofile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'conferences.balance': {
            'Meta': {'object_name': 'Balance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'conferences.conference': {
            'Meta': {'object_name': 'Conference'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'conference_durations'", 'to': u"orm['conferences.TimePeriod']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'publications_submission_period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'publications_submissions'", 'to': u"orm['conferences.TimePeriod']"}),
            'registration_periods': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'registration_periods'", 'symmetrical': 'False', 'to': u"orm['conferences.TimePeriod']"}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True'}),
            'summaries_submission_period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'summaries_submissions'", 'to': u"orm['conferences.TimePeriod']"})
        },
        u'conferences.conferencesfile': {
            'Meta': {'object_name': 'ConferencesFile'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'conferences.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'lectures_dates'", 'to': u"orm['conferences.TimePeriod']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referents': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'lectures'", 'to': u"orm['conferences.Session']"}),
            'summary': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conferences.Summary']", 'unique': 'True'})
        },
        u'conferences.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'balance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.Balance']"}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'full_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'time_to_pay': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'payments'", 'to': u"orm['conferences.TimePeriod']"})
        },
        u'conferences.publication': {
            'Meta': {'object_name': 'Publication', '_ormbases': [u'conferences.ConferencesFile']},
            u'conferencesfile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conferences.ConferencesFile']", 'unique': 'True', 'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'publications'", 'to': u"orm['conferences.Lecture']"})
        },
        u'conferences.review': {
            'Meta': {'object_name': 'Review'},
            'accepted': ('django.db.models.fields.BooleanField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'file_reviewed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.ConferencesFile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.Reviewer']"}),
            'unguessable_id': ('django.db.models.fields.CharField', [], {'default': "u'9UjrSPA8uLKlLBHb8JogVvpVwxOzRL4s'", 'unique': 'True', 'max_length': '32'})
        },
        u'conferences.reviewer': {
            'Meta': {'object_name': 'Reviewer'},
            'availability': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'reviewer_availability'", 'symmetrical': 'False', 'to': u"orm['conferences.TimePeriod']"}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'unavailability': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'reviewer_unavailability'", 'symmetrical': 'False', 'to': u"orm['conferences.TimePeriod']"}),
            'user_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'conferences.session': {
            'Meta': {'object_name': 'Session'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'sessions'", 'to': u"orm['conferences.Conference']"}),
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'sessions_dates'", 'to': u"orm['conferences.TimePeriod']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'topic': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conferences.Topic']", 'unique': 'True'})
        },
        u'conferences.summary': {
            'Meta': {'object_name': 'Summary', '_ormbases': [u'conferences.ConferencesFile']},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'summaries'", 'to': u"orm['conferences.Conference']"}),
            u'conferencesfile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conferences.ConferencesFile']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'conferences.timeperiod': {
            'Meta': {'object_name': 'TimePeriod'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'conferences.topic': {
            'Meta': {'object_name': 'Topic'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.Conference']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'super_topic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'sub_topics'", 'null': 'True', 'to': u"orm['conferences.Topic']"})
        },
        u'conferences.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'all_files'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_files'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_filer.file_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folder': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_owned_folders'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['conferences']