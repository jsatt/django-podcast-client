# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PodcastChannel.slug'
        db.alter_column(u'podcast_client_podcastchannel', 'slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', populate_from='title', overwrite=True))
        # Adding field 'PodcastItem.slug'
        db.add_column(u'podcast_client_podcastitem', 'slug',
                      self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, default='', populate_from=('channel', 'title'), overwrite=False),
                      keep_default=False)

        # Adding field 'PodcastItem.link'
        db.add_column(u'podcast_client_podcastitem', 'link',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'PodcastItem.cover_url'
        db.add_column(u'podcast_client_podcastitem', 'cover_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'PodcastChannel.slug'
        db.alter_column(u'podcast_client_podcastchannel', 'slug', self.gf('django_extensions.db.fields.AutoSlugField')(populate_from='title', allow_duplicates=False, max_length=50, separator=u'-', overwrite=False))
        # Deleting field 'PodcastItem.slug'
        db.delete_column(u'podcast_client_podcastitem', 'slug')

        # Deleting field 'PodcastItem.link'
        db.delete_column(u'podcast_client_podcastitem', 'link')

        # Deleting field 'PodcastItem.cover_url'
        db.delete_column(u'podcast_client_podcastitem', 'cover_url')


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
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'podcast_client.podcastitem': {
            'Meta': {'ordering': "('-publish_date',)", 'object_name': 'PodcastItem'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'podcast_items'", 'to': u"orm['podcast_client.PodcastChannel']"}),
            'cover_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'listened': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "('channel', 'title')", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['podcast_client']