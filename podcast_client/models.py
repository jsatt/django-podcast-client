from xml.dom import minidom
from lxml import etree
import logging

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django_extensions.db.models import AutoSlugField, TimeStampedModel
import dateutil.parser
import requests

logger = logging.getLogger(__name__)


class PodcastChannel(TimeStampedModel):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    copyright = models.CharField(max_length=255, blank=True)
    cover_url = models.URLField(blank=True)
    download_new = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.title or self.url

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
            self.title = getattr(channel.find('title'), 'text', '')
            self.description = getattr(channel.find('description'), 'text', '')
            self.website = getattr(channel.find('link'), 'text', '')
            self.copyright = getattr(channel.find('copyright'), 'text', '')
            self.cover_url = self.parse_cover_url(channel)
            self.save()
            self.update_items(channel, download=download)
        else:
            logger.error('Failed to retrieve feed. Status %s' % req.reason)


    def parse_cover_url(self, tree):
        image_url = getattr(tree.find('image/url'), 'text', '')

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
            guid = getattr(item.find('guid'), 'text', '')
            pod_item, created = self.podcast_items.get_or_create(guid=guid)
            if created:
                pod_item.title = getattr(item.find('title'), 'text', '')
                pod_item.description = getattr(
                    item.find('description'), 'text', '')
                pod_item.author = getattr(item.find('author'), 'text', '')
                pub_date = getattr(item.find('pubDate'), 'text', '')
                if pub_date:
                    pod_item.publish_date = dateutil.parser.parse(pub_date)
                enclosure = getattr(item.find('enclosure'), 'attrib', '')
                if enclosure:
                    pod_item.url = enclosure.get('url', '')
                    pod_item.file_type = enclosure.get('type', '')
                pod_item.save()
                new_items.append(pod_item)
        logger.info('Found %d new items' % len(new_items))
        if self.download_new or download:
            for item in new_items:
                item.download_file()


class PodcastItem(models.Model):
    guid = models.CharField(max_length=255, db_index=True)
    channel = models.ForeignKey(PodcastChannel, related_name='podcast_items')
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255, blank=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    file_type = models.CharField(max_length=20, blank=True)
    file = models.FileField(upload_to='files', blank=True, null=True)
    listened = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s - %s' % (self.channel, self.title, self.publish_date)

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


def cleanup_item_delete(sender, instance=None, **kwargs):
    instance.delete_file()

models.signals.pre_delete.connect(
    cleanup_item_delete, sender=PodcastItem)
