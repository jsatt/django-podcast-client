from lxml import etree
import logging

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django_extensions.db.models import AutoSlugField, TimeStampedModel
import dateutil.parser
import requests

logger = logging.getLogger(__name__)

settings.PODCAST_DIRECTORY = getattr(settings, 'PODCAST_DIRECTORY', 'podcasts')

class PodcastChannel(TimeStampedModel):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='title', overwrite=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    copyright = models.CharField(max_length=255, blank=True)
    cover_url = models.URLField(blank=True)
    download_new = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.title or self.url)

    @classmethod
    def subscribe(cls, url):
        channel = cls(url=url)
        channel.update_channel()
        return channel

    def update_channel(self, download=False):
        logger.info('Updating Channel: %s' % self)
        req = requests.get(self.url)
        if req.ok:
            tree = etree.fromstring(req.content)
            channel = tree.find('channel')
            self.title = getattr(channel.find('title'), 'text', None) or ''
            self.description = getattr(
                channel.find('description'), 'text', None) or ''
            self.website = getattr(
                channel.find('link'), 'text', None or '')
            self.copyright = getattr(
                channel.find('copyright'), 'text', None) or ''
            self.cover_url = self.parse_cover_url(channel)
            self.save()
            self.update_items(channel, download=download)
        else:
            logger.error('Failed to retrieve feed. Status %s' % req.reason)


    def parse_cover_url(self, tree):
        image_url = getattr(
            tree.find('image/url'), 'text', None) or ''

        if not image_url and 'media' in tree.nsmap:
            image_url = getattr(
                tree.find('media:thumbnail', tree.nsmap),
                'attrib', {}).get('url', '')

        if not image_url and 'itunes' in tree.nsmap:
            image_url = getattr(
                tree.find('itunes:image', tree.nsmap),
                'attrib', {}).get('href', '')

        return image_url


    def update_items(self, channel, download=False):
        new_items = []
        for item in channel.findall('item'):
            guid = getattr(item.find('guid'), 'text', None) or ''
            pod_item, created = self.podcast_items.get_or_create(guid=guid)
            if created:
                pod_item.title = getattr(
                    item.find('title'), 'text', None) or ''
                pod_item.description = getattr(
                    item.find('description'), 'text', None) or ''
                pod_item.author = getattr(
                    item.find('author'), 'text', None)or ''
                pod_item.link = getattr(item.find('link'), 'text', None) or ''
                pub_date = getattr(item.find('pubDate'), 'text', None) or ''
                if pub_date:
                    pod_item.publish_date = dateutil.parser.parse(pub_date)
                enclosure = getattr(
                    item.find('enclosure'), 'attrib', None) or ''
                if enclosure:
                    pod_item.url = enclosure.get('url', '')
                    pod_item.file_type = enclosure.get('type', '')
                pod_item.cover_url = self.parse_cover_url(item)
                pod_item.save()
                new_items.append(pod_item)
        logger.info('Found %d new items' % len(new_items))
        if self.download_new or download:
            for item in new_items:
                item.download_file()

    def has_unlistened(self):
        return self.podcast_items.filter(listened=False).exists()


class PodcastItem(models.Model):
    guid = models.CharField(max_length=255, db_index=True)
    channel = models.ForeignKey(PodcastChannel, related_name='podcast_items')
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from=('channel', 'title'))
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    file_type = models.CharField(max_length=20, blank=True)
    file = models.FileField(upload_to=settings.PODCAST_DIRECTORY, blank=True,
                            null=True)
    listened = models.BooleanField(default=False)
    cover_url = models.URLField(blank=True)

    AUDIO_FORMATS = ('audio/mpeg', 'audio/mp4', 'audio/ogg', 'audio/vorbis',
                     'audio/webm', 'audio/vnd.wave')
    VIDEO_FORMATS = ('video/mpeg', 'video/mp4', 'video/ogg', 'video/webm',
                     'video/quicktime', 'video/x-flv', 'video/x-ms-wmv',
                     'video/x-m4v')

    class Meta:
        get_latest_by = 'publish_date'
        ordering = ('-publish_date',)

    def __unicode__(self):
        return u'%s - %s' % (self.channel, self.title)

    def download_file(self):
        logger.info('Downloading - %s' % self.title)
        req = requests.get(self.url)
        if req.ok:
            file = SimpleUploadedFile(
                self.url, req.content, req.headers['content-type'])
            self.file.save(self.url, file)
        else:
            logger.error('Failed to retrieve file. Status %s' % req.reason)

    def delete_file(self):
        if self.file:
            self.file.delete()

    @property
    def media_type(self):
        if self.file_type in self.AUDIO_FORMATS:
            media_type = 'audio'
        elif self.file_type in self.VIDEO_FORMATS:
            media_type = 'video'
        elif self.file_type:
            media_type = 'unknown'
        else:
            media_type = 'none'
        return media_type


def cleanup_item_delete(sender, instance=None, **kwargs):
    instance.delete_file()

models.signals.pre_delete.connect(
    cleanup_item_delete, sender=PodcastItem)
