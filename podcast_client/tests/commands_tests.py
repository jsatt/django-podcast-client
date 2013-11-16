from django.core.management import call_command
from django.test import TestCase
import mox
import requests

from podcast_client.models import PodcastChannel
from podcast_client.tests import Struct


class PodcastManagementCmdTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.stdout = Struct(
            write=lambda x: self.stdout.lines.append(x), lines=[])
        self.stderr = Struct(
            write=lambda x: self.stderr.lines.append(x), lines=[])
        self.channel1 = PodcastChannel.objects.create(
            url='testurl.com/podcast', title='Test url')
        self.channel2 = PodcastChannel.objects.create(
            url='other.com/radio', title='Other url')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_list(self):
        call_command('podcast', list=True, stdout=self.stdout,
                     stderr=self.stderr)
        self.assertEqual(len(self.stderr.lines), 0)
        self.assertEqual(len(self.stdout.lines), 2)
        self.assertIn('Test url (test-url)\n', self.stdout.lines)
        self.assertIn('Other url (other-url)\n', self.stdout.lines)

    def test_subscribe(self):
        self.mock.StubOutWithMock(PodcastChannel, 'subscribe')
        PodcastChannel.subscribe('newurl.com')

        self.mock.ReplayAll()
        call_command('podcast', 'newurl.com', subscribe=True,
                     stdout=self.stdout, stderr=self.stderr)
        self.mock.VerifyAll()

        self.assertEqual(len(self.stderr.lines), 0)
        self.assertEqual(len(self.stdout.lines), 0)

    def test_subscribe_failed_request(self):
        self.mock.StubOutWithMock(PodcastChannel, 'subscribe')
        PodcastChannel.subscribe('newurl.com').AndRaise(
            requests.exceptions.RequestException)

        self.mock.ReplayAll()
        call_command('podcast', 'newurl.com', subscribe=True,
                     stdout=self.stdout, stderr=self.stderr)
        self.mock.VerifyAll()

        self.assertEqual(len(self.stderr.lines), 1)
        self.assertEqual(len(self.stdout.lines), 0)
        self.assertEqual(
            self.stderr.lines[0],
            '"newurl.com" is not a valid url. Skipping.\n')

    def test_unsubscribe(self):
        self.mock.StubOutWithMock(PodcastChannel, 'delete')
        PodcastChannel.delete()

        self.mock.ReplayAll()
        call_command('podcast', 'test-url', unsubscribe=True,
                     stdout=self.stdout, stderr=self.stderr)
        self.mock.VerifyAll()

        self.assertEqual(len(self.stderr.lines), 0)
        self.assertEqual(len(self.stdout.lines), 1)
        self.assertEqual(
            self.stdout.lines[0], '"Test url" unsubscribed and deleted.\n')

    def test_unsubscribe_invalid_slug_fails(self):
        self.mock.StubOutWithMock(PodcastChannel, 'delete')

        self.mock.ReplayAll()
        call_command('podcast', 'fake-feed', unsubscribe=True,
                     stdout=self.stdout, stderr=self.stderr)
        self.mock.VerifyAll()

        self.assertEqual(len(self.stderr.lines), 1)
        self.assertEqual(
            self.stderr.lines[0],
            'Please enter a valid slug. Use -l or --list to '
            'see all available slugs.\n')
        self.assertEqual(len(self.stdout.lines), 0)

    def test_update_no_args(self):
        self.mock.StubOutWithMock(PodcastChannel, 'update_channel')
        self.channel2.update_channel(download=None)
        self.channel1.update_channel(download=None)

        self.mock.ReplayAll()
        call_command('podcast', update=True, stdout=self.stdout,
                     stderr=self.stderr)
        self.mock.VerifyAll()
        self.assertEqual(len(self.stderr.lines), 0)
        self.assertEqual(len(self.stdout.lines), 0)

    def test_update_channel(self):
        self.mock.StubOutWithMock(PodcastChannel, 'update_channel')
        self.channel1.update_channel(download=None)

        self.mock.ReplayAll()
        call_command('podcast', 'test-url', update=True,
                     stdout=self.stdout, stderr=self.stderr)
        self.mock.VerifyAll()
        self.assertEqual(len(self.stderr.lines), 0)
        self.assertEqual(len(self.stdout.lines), 0)

    def test_update_invalid_channel(self):
        self.mock.StubOutWithMock(PodcastChannel, 'update_channel')
        self.mock.ReplayAll()
        call_command('podcast', 'fake-feed', update=True,
                     stdout=self.stdout, stderr=self.stderr)
        self.mock.VerifyAll()
        self.assertEqual(len(self.stderr.lines), 1)
        self.assertEqual(len(self.stdout.lines), 0)
        self.assertEqual(
            self.stderr.lines[0],
            'Please enter at least one valid slug or no slugs to update '
            'all. Use -l or --list to see all available slugs.\n')

    def test_not_args_does_nothing(self):
        call_command('podcast', stdout=self.stdout, stderr=self.stderr)

        self.assertEqual(len(self.stderr.lines), 0)
        self.assertEqual(len(self.stdout.lines), 0)
