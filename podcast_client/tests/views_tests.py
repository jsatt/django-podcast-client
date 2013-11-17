from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework import generics
import mox

from podcast_client import app as celery_app, views
from podcast_client.api import serializers
from podcast_client.models import PodcastChannel, PodcastItem

try:
    import celery as celery_installed
except ImportError:
    celery_installed = None


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

    def test_get_download_file(self):
        channel = PodcastChannel()
        item = PodcastItem(id=52, channel=channel)
        request = RequestFactory().get('')
        request.DATA = {'download_file': ''}
        self.mock.StubOutWithMock(self.view, 'get_object')
        self.mock.StubOutWithMock(celery_app.tasks, 'download_file')
        self.mock.StubOutWithMock(self.view, 'get_serializer')
        self.view.get_object().AndReturn(item)
        celery_app.tasks.download_file(52)
        mock_serializer = self.mock.CreateMockAnything()
        mock_serializer.data = {'serialized': 'data'}
        self.view.get_serializer({'status': 'DONE'}).AndReturn(mock_serializer)
        
        self.mock.ReplayAll()
        resp = self.view.get(request)
        self.mock.VerifyAll()

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.data, {"serialized": "data"})

    def test_get_download_file_celery(self):
        if celery_installed:
            channel = PodcastChannel.objects.create()
            item = PodcastItem.objects.create(id=52, channel=channel)
            request = RequestFactory().get('')
            request.DATA = {'download_file': ''}
            self.mock.StubOutWithMock(self.view, 'get_object')
            self.mock.StubOutWithMock(celery_app.tasks, 'download_file')
            self.mock.StubOutWithMock(celery_app.tasks.download_file, 'delay')
            self.mock.StubOutWithMock(self.view, 'get_serializer')
            self.view.get_object().AndReturn(item)
            celery_app.tasks.download_file.delay(52)
            mock_serializer = self.mock.CreateMockAnything()
            mock_serializer.data = {'serialized': 'data'}
            self.view.get_serializer({'status': 'DONE'}).AndReturn(mock_serializer)
            
            self.mock.ReplayAll()
            resp = self.view.get(request)
            self.mock.VerifyAll()

            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.data, {"serialized": "data"})
