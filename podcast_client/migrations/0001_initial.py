# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PodcastChannel'
        db.create_table(u'podcast_client_podcastchannel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('cover_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('download_new', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'podcast_client', ['PodcastChannel'])

        # Adding model 'PodcastItem'
        db.create_table(u'podcast_client_podcastitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='podcast_items', to=orm['podcast_client.PodcastChannel'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('file_type', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('listened', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'podcast_client', ['PodcastItem'])


    def backwards(self, orm):
        # Deleting model 'PodcastChannel'
        db.delete_table(u'podcast_client_podcastchannel')

        # Deleting model 'PodcastItem'
        db.delete_table(u'podcast_client_podcastitem')


    models = {
        u'podcast_client.podcastchannel': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'PodcastChannel'},
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cover_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'download_new': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'podcast_client.podcastitem': {
            'Meta': {'object_name': 'PodcastItem'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'podcast_items'", 'to': u"orm['podcast_client.PodcastChannel']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listened': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['podcast_client']