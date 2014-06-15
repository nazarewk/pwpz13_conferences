# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Payment.is_confirmed'
        db.add_column(u'conferences_payment', 'is_confirmed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Payment.is_confirmed'
        db.delete_column(u'conferences_payment', 'is_confirmed')


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
            'available': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'balance'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'conferences.conference': {
            'Meta': {'object_name': 'Conference'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'conference_admins'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'duration': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'conference_duration'", 'unique': 'True', 'null': 'True', 'to': u"orm['conferences.TimePeriod']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'publications_submission_period': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'publications_submission'", 'unique': 'True', 'null': 'True', 'to': u"orm['conferences.TimePeriod']"}),
            'registered_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'conference_registered_users'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'registration_periods': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'registration_periods'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['conferences.TimePeriod']"}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'summaries_submission_period': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'summaries_submission'", 'unique': 'True', 'null': 'True', 'to': u"orm['conferences.TimePeriod']"})
        },
        u'conferences.conferencesfile': {
            'Meta': {'object_name': 'ConferencesFile', '_ormbases': ['filer.File']},
            u'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'PR'", 'max_length': '2'})
        },
        u'conferences.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'duration': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'lectures_dates'", 'unique': 'True', 'to': u"orm['conferences.TimePeriod']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referents': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'lectures'", 'to': u"orm['conferences.Session']"}),
            'summary': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conferences.Summary']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'conferences.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'balance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'payments'", 'to': u"orm['conferences.Balance']"}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "u'PLN'", 'max_length': '3'}),
            'full_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'summary': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'payment'", 'unique': 'True', 'null': 'True', 'to': u"orm['conferences.Summary']"}),
            'time_to_pay': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'payment'", 'unique': 'True', 'to': u"orm['conferences.TimePeriod']"})
        },
        u'conferences.price': {
            'Meta': {'object_name': 'Price'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pricing'", 'to': u"orm['conferences.Conference']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'})
        },
        u'conferences.publication': {
            'Meta': {'object_name': 'Publication', '_ormbases': [u'conferences.ConferencesFile']},
            u'conferencesfile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conferences.ConferencesFile']", 'unique': 'True', 'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'publications'", 'to': u"orm['conferences.Lecture']"})
        },
        u'conferences.review': {
            'Meta': {'object_name': 'Review'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'file_reviewed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.ConferencesFile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.Reviewer']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'NO'", 'max_length': '2'}),
            'unguessable_id': ('django.db.models.fields.CharField', [], {'default': "u'hHKZRYkYcxxBcEcVqceBPFufAIyi8w5i'", 'unique': 'True', 'max_length': '32'})
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
            'user_account': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'conferences.session': {
            'Meta': {'object_name': 'Session'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'session_admins'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'sessions'", 'to': u"orm['conferences.Conference']"}),
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'sessions_dates'", 'to': u"orm['conferences.TimePeriod']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'registered_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'session_registered_users'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
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
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'topics'", 'to': u"orm['conferences.Conference']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['conferences.Topic']"})
        },
        u'conferences.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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