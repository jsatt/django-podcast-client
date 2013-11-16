from datetime import datetime
from lxml import etree

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.test import TestCase
from django.utils import timezone
import mox
import requests

from podcast_client.models import (logger as model_logger, PodcastChannel,
                                   PodcastItem)
from podcast_client.tests import Struct


class PodcastChannelModelTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_unicode(self):
        channel = PodcastChannel(url='http://example.com', title='Fake Feed')
        self.assertEqual(unicode(channel), u'Fake Feed')

    def test_unicode_wo_title(self):
        channel = PodcastChannel(url='http://example.com')
        self.assertEqual(unicode(channel), u'http://example.com')

    def test_subscribe(self):
        self.mock.StubOutWithMock(PodcastChannel, 'update_channel')
        PodcastChannel.update_channel()

        self.mock.ReplayAll()
        sub_channel = PodcastChannel.subscribe('http://test.com')
        self.mock.VerifyAll()

        self.assertEqual(sub_channel.url, 'http://test.com')

    def test_update_channel(self):
        feed_content = '''
        <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
            <channel>
                <title>Fake Feed</title>
                <link>http://example.com</link>
                <description>This is a sample feed.</description>
                <copyright>All rights reserved.</copyright>
                <pubDate>Sun, 02 Sep 2012 18:17:35 -0700</pubDate>
                <category>Sample stuff</category>
                <category>News</category>
                <image>
                    <url>http://example.com/feed.jpg</url>
                </image>
                <item><title>Episode 123</title></item>
            </channel>
        </rss>
        '''
        feed_response = Struct(
            status_code=200, ok=True, content=feed_content,
            url='http://test.com')
        self.mock.StubOutWithMock(requests, 'get')
        requests.get('http://test.com').AndReturn(feed_response)
        self.mock.StubOutWithMock(PodcastChannel, 'parse_cover_url')
        PodcastChannel.parse_cover_url(mox.IsA(etree._Element)).AndReturn(
            'http://example.com/feed.jpg')
        self.mock.StubOutWithMock(PodcastChannel, 'save')
        PodcastChannel.save()
        self.mock.StubOutWithMock(PodcastChannel, 'update_items')
        PodcastChannel.update_items(mox.IsA(etree._Element), download=True)
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Updating Channel: Old Title')

        channel = PodcastChannel(url='http://test.com', title='Old Title')

        self.mock.ReplayAll()
        channel.update_channel(download=True)
        self.mock.VerifyAll()

        self.assertEqual(channel.title, 'Fake Feed')
        self.assertEqual(channel.description, 'This is a sample feed.')
        self.assertEqual(channel.cover_url, 'http://example.com/feed.jpg')
        self.assertEqual(channel.website, 'http://example.com')
        self.assertEqual(channel.copyright, 'All rights reserved.')

    def test_update_channel_bad_response(self):
        feed_response = Struct(status_code=404, ok=False, reason='404')
        self.mock.StubOutWithMock(requests, 'get')
        requests.get('http://test.com').AndReturn(feed_response)
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Updating Channel: http://test.com')
        self.mock.StubOutWithMock(model_logger, 'error')
        model_logger.error('Failed to retrieve feed. Status 404')
        self.mock.StubOutWithMock(PodcastChannel, 'parse_cover_url')
        self.mock.StubOutWithMock(PodcastChannel, 'save')
        self.mock.StubOutWithMock(PodcastChannel, 'update_items')
        channel = PodcastChannel(url='http://test.com')

        self.mock.ReplayAll()
        channel.update_channel(download=True)
        self.mock.VerifyAll()

        self.assertEqual(channel.title, '')
        self.assertEqual(channel.description, '')
        self.assertEqual(channel.cover_url, '')

    def test_parse_cover_url_image_tage(self):
        feed_content = '''
        <rss version="2.0">
            <channel>
                <title>Fake Feed</title>
                <image>
                    <url>http://example.com/feed.jpg</url>
                </image>
                <item><title>Episode 123</title></item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')

        self.assertEqual(PodcastChannel().parse_cover_url(tree),
                         'http://example.com/feed.jpg')

    def test_parse_cover_url_media_thumbnail(self):
        feed_content = '''
        <rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
            <channel>
                <title>Fake Feed</title>
                <media:thumbnail url="http://example.com/feed.jpg" />
                <item><title>Episode 123</title></item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')

        self.assertEqual(PodcastChannel().parse_cover_url(tree),
                         'http://example.com/feed.jpg')

    def test_parse_cover_url_itunes_image(self):
        feed_content = '''
        <rss version="2.0" xmlns:itunes="http://www.itunes.com/podcast-1.0">
            <channel>
                <title>Fake Feed</title>
                <itunes:image href="http://example.com/feed.jpg" />
                <item><title>Episode 123</title></item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')

        self.assertEqual(PodcastChannel().parse_cover_url(tree),
                         'http://example.com/feed.jpg')

    def test_update_items_new_item(self):
        feed_content = '''
        <rss version="2.0">
            <channel>
                <title>Fake Feed</title>
                <item>
                    <title>Episode 123</title>
                    <description>Another episode</description>
                    <author>jim@example.com (Jim Bob)</author>
                    <link>http://example.com/ep123/</link>
                    <image><url>http://example.com/feed.jpg</url></image>
                    <pubDate>Mon, 25 Feb 2013 07:10:42 -0000</pubDate>
                    <guid isPermaLink="false">/ep123.mp3</guid>
                    <enclosure url="http://example.com/ep123.mp3"
                        type="audio/mpeg" />
                </item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')
        channel = PodcastChannel.objects.create(url='http://example.com')

        self.mock.StubOutWithMock(PodcastItem, 'download_file')
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Found 1 new items')
        self.mock.StubOutWithMock(PodcastChannel, 'parse_cover_url')
        PodcastChannel.parse_cover_url(mox.IsA(etree._Element)).AndReturn(
            'http://example.com/feed.jpg')

        self.mock.ReplayAll()
        channel.update_items(tree)
        self.mock.VerifyAll()

        item = channel.podcast_items.get()
        self.assertEqual(channel.podcast_items.count(), 1)
        self.assertEqual(item.guid, '/ep123.mp3')
        self.assertEqual(item.title, 'Episode 123')
        self.assertEqual(item.description, 'Another episode')
        self.assertEqual(item.author, 'jim@example.com (Jim Bob)')
        self.assertEqual(item.link, 'http://example.com/ep123/')
        self.assertEqual(item.publish_date,
                         datetime(2013, 2, 25, 7, 10, 42, tzinfo=timezone.utc))
        self.assertEqual(item.url, 'http://example.com/ep123.mp3')
        self.assertEqual(item.file_type, 'audio/mpeg')
        self.assertEqual(item.cover_url, 'http://example.com/feed.jpg')

    def test_update_items_existing_item(self):
        feed_content = '''
        <rss version="2.0">
            <channel>
                <title>Fake Feed</title>
                <item>
                    <title>Episode 123</title>
                    <description>Another episode</description>
                    <author>jim@example.com (Jim Bob)</author>
                    <pubDate>Mon, 25 Feb 2013 07:10:42 -0000</pubDate>
                    <guid isPermaLink="false">/ep123.mp3</guid>
                    <enclosure url="http://example.com/ep123.mp3"
                        type="audio/mpeg" />
                </item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')
        channel = PodcastChannel.objects.create(url='http://example.com')
        channel.podcast_items.create(guid='/ep123.mp3', title='Old title')

        self.mock.StubOutWithMock(PodcastItem, 'download_file')
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Found 0 new items')

        self.mock.ReplayAll()
        channel.update_items(tree)
        self.mock.VerifyAll()

        item = channel.podcast_items.get()
        self.assertEqual(item.title, 'Old title')

    def test_update_items_empty_feed(self):
        feed_content = '''
        <rss version="2.0">
            <channel>
                <title>Fake Feed</title>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')
        channel = PodcastChannel.objects.create(url='http://example.com')

        self.mock.StubOutWithMock(PodcastItem, 'download_file')
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Found 0 new items')

        self.mock.ReplayAll()
        channel.update_items(tree)
        self.mock.VerifyAll()

        self.assertEqual(channel.podcast_items.count(), 0)

    def test_update_items_partial_item(self):
        feed_content = '''
        <rss version="2.0">
            <channel>
                <title>Fake Feed</title>
                <item>
                    <guid isPermaLink="false">/ep123.mp3</guid>
                </item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')
        channel = PodcastChannel.objects.create(url='http://example.com')

        self.mock.StubOutWithMock(PodcastItem, 'download_file')
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Found 1 new items')

        self.mock.ReplayAll()
        channel.update_items(tree)
        self.mock.VerifyAll()

        item = channel.podcast_items.get()
        self.assertEqual(channel.podcast_items.count(), 1)
        self.assertEqual(item.guid, '/ep123.mp3')
        self.assertEqual(item.title, '')
        self.assertEqual(item.description, '')
        self.assertEqual(item.author, '')
        self.assertEqual(item.publish_date, None)
        self.assertEqual(item.url, '')
        self.assertEqual(item.file_type, '')

    def test_update_items_download_new_for_feed(self):
        feed_content = '''
        <rss version="2.0">
            <channel>
                <title>Fake Feed</title>
                <item>
                    <guid isPermaLink="false">/ep123.mp3</guid>
                    <enclosure url="http://example.com/ep123.mp3"
                        type="audio/mpeg" />
                </item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')
        channel = PodcastChannel.objects.create(
            url='http://example.com', download_new=True)

        self.mock.StubOutWithMock(PodcastItem, 'download_file')
        PodcastItem.download_file()
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Found 1 new items')

        self.mock.ReplayAll()
        channel.update_items(tree)
        self.mock.VerifyAll()

        item = channel.podcast_items.get()
        self.assertEqual(channel.podcast_items.count(), 1)
        self.assertEqual(item.guid, '/ep123.mp3')

    def test_update_items_download_arg_true(self):
        feed_content = '''
        <rss version="2.0">
            <channel>
                <title>Fake Feed</title>
                <item>
                    <guid isPermaLink="false">/ep123.mp3</guid>
                    <enclosure url="http://example.com/ep123.mp3"
                        type="audio/mpeg" />
                </item>
            </channel>
        </rss>
        '''
        tree = etree.fromstring(feed_content).find('channel')
        channel = PodcastChannel.objects.create(url='http://example.com')

        self.mock.StubOutWithMock(PodcastItem, 'download_file')
        PodcastItem.download_file()
        self.mock.StubOutWithMock(model_logger, 'info')
        model_logger.info('Found 1 new items')

        self.mock.ReplayAll()
        channel.update_items(tree, download=True)
        self.mock.VerifyAll()

        item = channel.podcast_items.get()
        self.assertEqual(channel.podcast_items.count(), 1)
        self.assertEqual(item.guid, '/ep123.mp3')

    def test_has_unlistened(self):
        channel = PodcastChannel.objects.create(url='http://example.com')
        channel.podcast_items.create(guid='/ep123.mp3', title='Old title',
                                     listened=True)

        self.assertFalse(channel.has_unlistened())


class PodcastItemModelTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_unicode(self):
        channel = PodcastChannel(title='Fake Feed')
        item = PodcastItem(channel=channel, title='Episode 123')

        self.assertEqual(
            unicode(item), 'Fake Feed - Episode 123')

    # TODO write tests that don't try to write files
    #def test_download_file(self):
    #    self.mock.StubOutWithMock(requests, 'get')
    #    file_resp = Struct(
    #        status_code=200, ok=True, content='file content',
    #        headers={'content-type': 'audio/mpeg'},
    #        request=Struct(path_url='/ep123.mp3'))
    #    requests.get('http://example.com/ep123.mp3', stream=True).AndReturn(
    #        file_resp)
    #    self.mock.StubOutWithMock(model_logger, 'info')
    #    model_logger.info('Downloading - Episode 123')
    #    self.mock.StubOutWithMock(FieldFile, 'save')
    #    self.mock.StubOutWithMock(models, 'mopen')
    #    models.mopen('/podcasts/ep123.mp3', 'wb')

    #    item = PodcastItem(url='http://example.com/ep123.mp3',
    #                       title='Episode 123')

    #    self.mock.ReplayAll()
    #    item.download_file()
    #    self.mock.VerifyAll()

    #def test_download_file_bad_response(self):
    #    self.mock.StubOutWithMock(requests, 'get')
    #    file_resp = Struct(status_code=404, ok=False, reason='404')
    #    requests.get('http://example.com/ep123.mp3', stream=True).AndReturn(
    #        file_resp)
    #    self.mock.StubOutWithMock(model_logger, 'info')
    #    model_logger.info('Downloading - Episode 123')
    #    self.mock.StubOutWithMock(model_logger, 'error')
    #    model_logger.error('Failed to retrieve file. Status 404')
    #    self.mock.StubOutWithMock(FieldFile, 'save')

    #    item = PodcastItem(url='http://example.com/ep123.mp3',
    #                       title='Episode 123')

    #    self.mock.ReplayAll()
    #    item.download_file()
    #    self.mock.VerifyAll()

    def test_delete_file(self):
        self.mock.StubOutWithMock(FieldFile, 'delete')
        FieldFile.delete()

        item = PodcastItem(
            file=SimpleUploadedFile('/ep123.txt', 'file contents'))

        self.mock.ReplayAll()
        item.delete_file()
        self.mock.VerifyAll()

    def test_delete_file_wo_file(self):
        self.mock.StubOutWithMock(FieldFile, 'delete')

        item = PodcastItem()

        self.mock.ReplayAll()
        item.delete_file()
        self.mock.VerifyAll()

    def test_cleanup_item_delete_signal(self):
        self.mock.StubOutWithMock(PodcastItem, 'delete_file')
        PodcastItem.delete_file()
        item = PodcastItem.objects.create(
            channel=PodcastChannel.objects.create(), guid='/ep123.mp3',
            url='http://example.com/ep123.mp3')

        self.mock.ReplayAll()
        item.delete()
        self.mock.VerifyAll()

    def test_media_type_audio(self):
        item = PodcastItem(file_type='audio/mpeg')
        self.assertEqual(item.media_type, 'audio')

    def test_media_type_video(self):
        item = PodcastItem(file_type='video/mpeg')
        self.assertEqual(item.media_type, 'video')

    def test_media_type_unknown(self):
        item = PodcastItem(file_type='image/jpeg')
        self.assertEqual(item.media_type, 'unknown')

    def test_media_type_none(self):
        pass
        item = PodcastItem()
        self.assertEqual(item.media_type, 'none')
