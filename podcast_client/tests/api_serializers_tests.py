from datetime import datetime

from django.test import TestCase
from django.utils.timezone import utc

from podcast_client.api import serializers
from podcast_client.models import PodcastChannel, PodcastItem


class PodcastChannelDetailSerializerTest(TestCase):
    def setUp(self):
        self.serializer = serializers.PodcastChannelDetailSerializer()

    def test_attrs(self):
        self.assertSequenceEqual(
            self.serializer.fields.keys(),
            ('url', 'api_url', 'title', 'slug', 'description', 'website',
             'copyright', 'cover_url', 'download_new', 'items',
             'has_unlistened'))
        self.assertSequenceEqual(
            self.serializer.Meta.read_only_fields,
            ('title', 'slug', 'description', 'website', 'copyright',
             'cover_url'))

    def test_get_latest_publish_date(self):
        channel = PodcastChannel.objects.create()
        PodcastItem.objects.create(
            channel=channel, publish_date=datetime(2013, 1, 1, tzinfo=utc))
        PodcastItem.objects.create(
            channel=channel, publish_date=datetime(2013, 3, 3, tzinfo=utc))

        latest_pub = self.serializer.get_latest_publish_date(channel)

        self.assertEqual(latest_pub, datetime(2013, 3, 3, tzinfo=utc))


class PodcastItemDetailSerializerTest(TestCase):
    def setUp(self):
        self.serializer = serializers.PodcastItemDetailSerializer()
        channel = PodcastChannel.objects.create()
        self.item = PodcastItem.objects.create(channel=channel)

    def test_attrs(self):
        self.assertSequenceEqual(
            self.serializer.fields.keys(),
            ('channel', 'url', 'api_url', 'title', 'slug', 'description',
             'author', 'link', 'publish_date', 'media_type', 'listened',
             'cover_url', 'file_downloaded'))
        self.assertSequenceEqual(
            self.serializer.Meta.read_only_fields,
            ('url', 'title', 'slug', 'description', 'author', 'link',
             'publish_date', 'cover_url'))

    def test_is_file_downloaded_false(self):
        self.assertFalse(self.serializer.is_file_downloaded(self.item))

    def test_is_file_downloaded_true(self):
        self.item.file = object()
        self.assertTrue(self.serializer.is_file_downloaded(self.item))
