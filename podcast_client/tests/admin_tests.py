from django.test import TestCase
from django.test.client import RequestFactory
import mox

from podcast_client.admin import PodcastChannelAdmin, PodcastItemAdmin
from podcast_client.models import PodcastChannel, PodcastItem


class PodcastChannelAdminTest(TestCase):
    def setUp(self):
        self.admin = PodcastChannelAdmin(PodcastChannel, 1)
        self.mock = mox.Mox()
        self.request = RequestFactory().get('')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_update_channels(self):
        channel1 = PodcastChannel()
        channel2 = PodcastChannel()
        qs = [channel1, channel2]

        self.mock.StubOutWithMock(channel1, 'update_channel')
        self.mock.StubOutWithMock(channel2, 'update_channel')
        channel1.update_channel()
        channel2.update_channel()

        self.mock.ReplayAll()
        self.admin.update_channels(self.request, qs)
        self.mock.VerifyAll()

    def test_save_model(self):
        channel = PodcastChannel()
        self.mock.StubOutWithMock(channel, 'save')
        self.mock.StubOutWithMock(channel, 'update_channel')
        channel.save()
        channel.update_channel()

        self.mock.ReplayAll()
        self.admin.save_model(self.request, channel, None, None)
        self.mock.VerifyAll()


class PodcastItemAdminTest(TestCase):
    def setUp(self):
        self.admin = PodcastItemAdmin(PodcastItem, 1)
        self.mock = mox.Mox()
        self.request = RequestFactory().get('')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_download_files(self):
        channel = PodcastChannel.objects.create()
        item1 = PodcastItem.objects.create(channel=channel)
        item2 = PodcastItem.objects.create(channel=channel)
        qs = [item1, item2]

        self.mock.StubOutWithMock(item1, 'download_file')
        self.mock.StubOutWithMock(item2, 'download_file')
        item1.download_file()
        item2.download_file()

        self.mock.ReplayAll()
        self.admin.download_files(self.request, qs)
        self.mock.VerifyAll()

    def test_delete_files(self):
        channel = PodcastChannel.objects.create()
        item1 = PodcastItem.objects.create(channel=channel)
        item2 = PodcastItem.objects.create(channel=channel)
        qs = [item1, item2]

        self.mock.StubOutWithMock(item1, 'delete_file')
        self.mock.StubOutWithMock(item2, 'delete_file')
        item1.delete_file()
        item2.delete_file()

        self.mock.ReplayAll()
        self.admin.delete_files(self.request, qs)
        self.mock.VerifyAll()

    def test_mark_as_listened(self):
        qs = PodcastItem.objects.all()
        self.mock.StubOutWithMock(qs, 'update')
        qs.update(listened=True)

        self.mock.ReplayAll()
        self.admin.mark_as_listened(self.request, qs)
        self.mock.VerifyAll()
