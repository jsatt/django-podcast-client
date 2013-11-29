from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework import generics
import mox

from podcast_client import views, tasks
from podcast_client.api import serializers
from podcast_client.models import PodcastChannel, PodcastItem


class ChannelDetailAPITest(TestCase):
    def test_attrs(self):
        view = views.ChannelDetailAPI()
        self.assertIsInstance(view, generics.RetrieveUpdateAPIView)
        self.assertEqual(view.model, PodcastChannel)
        self.assertEqual(
            view.serializer_class, serializers.PodcastChannelDetailSerializer)
        self.assertEqual(
            view.lookup_field, 'slug')


class ChannelListAPITest(TestCase):
    def test_attrs(self):
        view = views.ChannelListAPI()
        self.assertIsInstance(view, generics.ListCreateAPIView)
        self.assertEqual(view.model, PodcastChannel)
        self.assertEqual(
            view.serializer_class, serializers.PodcastChannelDetailSerializer)
        self.assertEqual(
            view.paginate_by, 10)


class ItemDetailAPITest(TestCase):
    def test_attrs(self):
        view = views.ItemDetailAPI()
        self.assertIsInstance(view, generics.RetrieveUpdateAPIView)
        self.assertEqual(view.model, PodcastItem)
        self.assertEqual(
            view.serializer_class, serializers.PodcastItemDetailSerializer)
        self.assertEqual(
            view.lookup_field, 'slug')


class ItemListAPITest(TestCase):
    def setUp(self):
        self.view = views.ItemListAPI()
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertIsInstance(self.view, generics.ListCreateAPIView)
        self.assertEqual(self.view.model, PodcastItem)
        self.assertEqual(
            self.view.serializer_class,
            serializers.PodcastItemDetailSerializer)
        self.assertEqual(
            self.view.paginate_by, 10)

    def test_get_queryset(self):
        self.view.kwargs = {'slug': 'channel-slug'}
        self.mock.StubOutWithMock(generics.ListCreateAPIView, 'get_queryset')
        queryset_mock = self.mock.CreateMockAnything()
        generics.ListCreateAPIView.get_queryset().AndReturn(queryset_mock)
        queryset_mock.filter(channel__slug='channel-slug').AndReturn(
            'filtered queryset')

        self.mock.ReplayAll()
        qs = self.view.get_queryset()
        self.mock.VerifyAll()

        self.assertEqual(qs, 'filtered queryset')


class ItemDeleteFileAPI(TestCase):
    def setUp(self):
        self.view = views.ItemFileAPI()
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertIsInstance(self.view, generics.GenericAPIView)

    def test_delete(self):
        item = PodcastItem()
        request = RequestFactory().get('')
        self.mock.StubOutWithMock(self.view, 'get_object')
        self.mock.StubOutWithMock(item, 'delete_file')
        self.view.get_object().AndReturn(item)
        item.delete_file()
        
        self.mock.ReplayAll()
        resp = self.view.delete(request)
        self.mock.VerifyAll()

        self.assertEqual(resp.status_code, 204)

    def test_get_download_file_celery(self):
        channel = PodcastChannel.objects.create()
        item = PodcastItem.objects.create(id=52, channel=channel)
        request = RequestFactory().get('', {'download_file': ''})
        self.mock.StubOutWithMock(self.view, 'get_object')
        self.mock.StubOutWithMock(tasks, 'download_file')
        self.mock.StubOutWithMock(tasks.download_file, 'delay')
        self.view.get_object().AndReturn(item)
        mock_task = self.mock.CreateMockAnything()
        mock_task.id = 1234
        mock_task.status = 'PENDING'
        tasks.download_file.delay(52).AndReturn(mock_task)
        
        self.mock.ReplayAll()
        resp = self.view.get(request)
        self.mock.VerifyAll()

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(
            resp.data, {"status": "PENDING", "task_id": 1234})
