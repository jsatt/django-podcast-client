from xml.dom import minidom

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django_extensions.db.models import AutoSlugField, TimeStampedModel
import dateutil.parser
import requests


class PodcastChannel(TimeStampedModel):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='title', overwrite=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers', blank=True, null=True)
    cover_url = models.URLField(blank=True)
    download_new = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.title or self.url

    @classmethod
    def subscribe(cls, url):
        channel = cls.objects.create(url=url)
        channel.update_channel()
        return channel

    def update_channel(self):
        print 'Updating Channel: %s' % self
        req = requests.get(self.url)
        assert req.ok, 'Failed to retrieve feed. Status %s' % req.reason
        channel = minidom.parseString(req.content).getElementsByTagName(
            'channel')[0]
        self.title = channel.getElementsByTagName('title')[0].firstChild.data
        self.description = channel.getElementsByTagName(
            'description')[0].firstChild.data
        cover_url = self.get_cover_image_url(channel)
        if cover_url and (not cover_url == self.cover_url or not self.cover):
            self.cover_url = cover_url
            self.download_cover()
        self.save()
        self.update_items(channel)

    def download_cover(self):
        req = requests.get(self.cover_url)
        assert req.ok, 'Failed to retrieve feed image. Status %s ' % req.reason
        file = SimpleUploadedFile(
            self.cover_url, req.content, req.headers['content-type'])
        self.cover.save(self.cover_url, file)

    def get_cover_image_url(self, channel):
        image_tag = channel.getElementsByTagName('image')
        if image_tag:
            image_url = image_tag[0].getElementsByTagName(
                'url')[0].firstChild.data
            if image_url:
                return image_url
        media_thumb = channel.getElementsByTagName('media:thumbnail')
        if media_thumb:
            return media_thumb[0].getAttribute('url')
        itunes_image = channel.getElementsByTagName('itunes:image')
        if itunes_image:
            return itunes_image[0].getAttribute('href')

    def save(self, *args, **kwargs):
        if not self.id:
            new = True
        else:
            new = False
        super(PodcastChannel, self).save(*args, **kwargs)
        if new:
            self.update_channel()

    def update_items(self, channel):
        new_items = []
        for item in channel.getElementsByTagName('item'):
            enclosure = item.getElementsByTagName('enclosure')
            if enclosure:
                guid = item.getElementsByTagName('guid')[0].firstChild.data
                pod_item, created = self.podcast_items.get_or_create(guid=guid)
                if created:
                    pod_item.url = enclosure[0].getAttribute('url')
                    pod_item.file_type = enclosure[0].getAttribute('type')
                    pod_item.title = item.getElementsByTagName(
                        'title')[0].firstChild.data
                    pod_item.description = item.getElementsByTagName(
                        'description')[0].firstChild.data
                    pod_item.publish_date = dateutil.parser.parse(
                        item.getElementsByTagName(
                            'pubDate')[0].firstChild.data)
                    pod_item.save()
                    new_items.append(pod_item)
        print 'Found %d new items' % len(new_items)
        if self.download_new:
            for item in new_items:
                item.download_file()


def cleanup_channel_delete(sender, instance=None, **kwargs):
    if instance.cover:
        instance.cover.delete()

models.signals.pre_delete.connect(
    cleanup_channel_delete, sender=PodcastChannel)


class PodcastItem(models.Model):
    guid = models.CharField(max_length=255, db_index=True)
    channel = models.ForeignKey(PodcastChannel, related_name='podcast_items')
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    file_type = models.CharField(max_length=20, blank=True)
    file = models.FileField(upload_to='files', blank=True, null=True)
    listened = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s - %s' % (self.channel, self.title, self.publish_date)

    def download_file(self):
        print 'Downloading - %s' % self.title
        req = requests.get(self.url)
        if not req.ok:
            print 'Failed to retrieve feed image. Status %s ' % req.reason
        file = SimpleUploadedFile(
            self.url, req.content, req.headers['content-type'])
        self.file.save(self.url, file)

    def delete_file(self):
        self.file.delete()


def cleanup_item_delete(sender, instance=None, **kwargs):
    if instance.file:
        instance.file.delete()

models.signals.pre_delete.connect(
    cleanup_item_delete, sender=PodcastItem)
