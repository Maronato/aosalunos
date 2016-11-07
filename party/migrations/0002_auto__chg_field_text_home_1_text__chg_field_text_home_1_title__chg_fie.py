# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Text.home_1_text'
        db.alter_column(u'party_text', 'home_1_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.home_1_title'
        db.alter_column(u'party_text', 'home_1_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Text.consu_1_text'
        db.alter_column(u'party_text', 'consu_1_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.consu_2_text'
        db.alter_column(u'party_text', 'consu_2_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.join_2_text'
        db.alter_column(u'party_text', 'join_2_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.join_1_text'
        db.alter_column(u'party_text', 'join_1_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.home_2_title'
        db.alter_column(u'party_text', 'home_2_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Text.us_1_title'
        db.alter_column(u'party_text', 'us_1_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Text.consu_1_title'
        db.alter_column(u'party_text', 'consu_1_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Text.join_1_title'
        db.alter_column(u'party_text', 'join_1_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Text.us_2_title'
        db.alter_column(u'party_text', 'us_2_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Text.home_2_text'
        db.alter_column(u'party_text', 'home_2_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.us_2_text'
        db.alter_column(u'party_text', 'us_2_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.us_1_text'
        db.alter_column(u'party_text', 'us_1_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Text.join_2_title'
        db.alter_column(u'party_text', 'join_2_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Text.consu_2_title'
        db.alter_column(u'party_text', 'consu_2_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Text.home_1_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.home_1_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.home_1_text'
        db.alter_column(u'party_text', 'home_1_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.home_1_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.home_1_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.home_1_title'
        db.alter_column(u'party_text', 'home_1_title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # User chose to not deal with backwards NULL issues for 'Text.consu_1_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.consu_1_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.consu_1_text'
        db.alter_column(u'party_text', 'consu_1_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.consu_2_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.consu_2_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.consu_2_text'
        db.alter_column(u'party_text', 'consu_2_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.join_2_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.join_2_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.join_2_text'
        db.alter_column(u'party_text', 'join_2_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.join_1_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.join_1_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.join_1_text'
        db.alter_column(u'party_text', 'join_1_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.home_2_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.home_2_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.home_2_title'
        db.alter_column(u'party_text', 'home_2_title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # User chose to not deal with backwards NULL issues for 'Text.us_1_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.us_1_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.us_1_title'
        db.alter_column(u'party_text', 'us_1_title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # User chose to not deal with backwards NULL issues for 'Text.consu_1_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.consu_1_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.consu_1_title'
        db.alter_column(u'party_text', 'consu_1_title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # User chose to not deal with backwards NULL issues for 'Text.join_1_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.join_1_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.join_1_title'
        db.alter_column(u'party_text', 'join_1_title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # User chose to not deal with backwards NULL issues for 'Text.us_2_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.us_2_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.us_2_title'
        db.alter_column(u'party_text', 'us_2_title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # User chose to not deal with backwards NULL issues for 'Text.home_2_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.home_2_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.home_2_text'
        db.alter_column(u'party_text', 'home_2_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.us_2_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.us_2_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.us_2_text'
        db.alter_column(u'party_text', 'us_2_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.us_1_text'
        raise RuntimeError("Cannot reverse this migration. 'Text.us_1_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.us_1_text'
        db.alter_column(u'party_text', 'us_1_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Text.join_2_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.join_2_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.join_2_title'
        db.alter_column(u'party_text', 'join_2_title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # User chose to not deal with backwards NULL issues for 'Text.consu_2_title'
        raise RuntimeError("Cannot reverse this migration. 'Text.consu_2_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Text.consu_2_title'
        db.alter_column(u'party_text', 'consu_2_title', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'app.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mod': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ra': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['misago.User']", 'unique': 'True'})
        },
        'misago.rank': {
            'Meta': {'object_name': 'Rank'},
            'as_tab': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'criteria': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'on_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['misago.Role']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'misago.role': {
            'Meta': {'object_name': 'Role'},
            '_permissions': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'permissions'", 'blank': 'True'}),
            '_special': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'special'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'misago.user': {
            'Meta': {'object_name': 'User'},
            '_avatar_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'avatar_crop'", 'blank': 'True'}),
            'acl_key': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'activation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'alerts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'alerts_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'allow_pds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'avatar_ban': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'avatar_ban_reason_admin': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar_ban_reason_user': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar_image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar_original': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar_temp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'email_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'follows': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'follows_set'", 'symmetrical': 'False', 'to': "orm['misago.User']"}),
            'hide_activity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ignores_set'", 'symmetrical': 'False', 'to': "orm['misago.User']"}),
            'is_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'join_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {}),
            'join_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'karma_given_n': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'karma_given_p': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'karma_n': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'karma_p': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'last_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'last_post': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_search': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_vote': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_date': ('django.db.models.fields.DateTimeField', [], {}),
            'posts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['misago.Rank']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'ranking': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'receive_newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['misago.Role']", 'symmetrical': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_ban': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signature_ban_reason_admin': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_ban_reason_user': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature_preparsed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subscribe_reply': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subscribe_start': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sync_pds': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'threads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'utc'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'unread_pds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username_slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'warning_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'warning_level_update_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'party.members': {
            'Meta': {'object_name': 'Members'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'github': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['app.Profile']", 'unique': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'party.promise': {
            'Meta': {'object_name': 'Promise'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'party.text': {
            'Meta': {'object_name': 'Text'},
            'consu_1_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'consu_1_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consu_2_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'consu_2_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'home_1_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'home_1_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'home_2_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'home_2_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_1_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'join_1_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'join_2_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'join_2_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'us_1_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'us_1_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'us_2_text': ('django.db.models.fields.TextField', [], {'default': "' '", 'null': 'True', 'blank': 'True'}),
            'us_2_title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['party']