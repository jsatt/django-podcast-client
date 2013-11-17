from django.test import TestCase
import mox

from podcast_client import tasks
from podcast_client.models import PodcastChannel, PodcastItem

try:
    import celery as celery_installed
except ImportError:
    celery_installed = None


class PodcastTasksTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.mock.StubOutWithMock(PodcastChannel, 'update_channel')
        self.channel1 = PodcastChannel.objects.create(
            url='testurl.com/podcast', title='Test url')
        self.channel2 = PodcastChannel.objects.create(
            url='other.com/radio', title='Other url')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_update_channel(self):
        self.channel1.update_channel(download=False)
        self.mock.ReplayAll()
        tasks.update_channel(self.channel1.slug)
        self.mock.VerifyAll()

        if celery_installed:
            self.assertTrue(hasattr(tasks.update_channel, 'apply_async'))

    def test_update_channel_force_download(self):
        self.channel1.update_channel(download=True)
        self.mock.ReplayAll()
        tasks.update_channel(self.channel1.slug, force_download=True)
        self.mock.VerifyAll()

    def test_update_all(self):
        self.channel1.update_channel(download=False)
        self.channel2.update_channel(download=False)
        self.mock.ReplayAll()
        tasks.update_all_channels()
        self.mock.VerifyAll()

        if celery_installed:
            self.assertTrue(hasattr(tasks.update_all_channels, 'apply_async'))

    def test_update_all_force_download(self):
        self.channel1.update_channel(download=True)
        self.channel2.update_channel(download=True)
        self.mock.ReplayAll()
        tasks.update_all_channels(force_download=True)
        self.mock.VerifyAll()

class DownloadFileTaskTest(TestCase):
    def setUp(self):
        channel = PodcastChannel.objects.create()
        self.item = PodcastItem.objects.create(id=33, channel=channel)
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_download_file(self):
        self.mock.StubOutWithMock(PodcastItem, 'download_file')
        PodcastItem.download_file()

        self.mock.ReplayAll()
        tasks.download_file(33)
        self.mock.VerifyAll()
