from rest_framework import status
from rest_framework.generics import (
    GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response

from . import tasks
from .api.serializers import (
    PodcastChannelDetailSerializer, PodcastItemDetailSerializer)
from .celery import app
from .models import PodcastChannel, PodcastItem


class ChannelDetailAPI(RetrieveUpdateAPIView):
    model = PodcastChannel
    serializer_class = PodcastChannelDetailSerializer
    lookup_field = 'slug'


class ChannelListAPI(ListCreateAPIView):
    model = PodcastChannel
    serializer_class = PodcastChannelDetailSerializer
    paginate_by = 10


class ItemDetailAPI(RetrieveUpdateAPIView):
    model = PodcastItem
    serializer_class = PodcastItemDetailSerializer
    lookup_field = 'slug'


class ItemListAPI(ListCreateAPIView):
    model = PodcastItem
    serializer_class = PodcastItemDetailSerializer
    paginate_by = 10

    def get_queryset(self):
        qs = super(ItemListAPI, self).get_queryset()
        return qs.filter(channel__slug=self.kwargs['slug'])


class ItemFileAPI(GenericAPIView):
    model = PodcastItem

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete_file()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {}

        if 'download_file' in request.GET:
            task = tasks.download_file.delay(self.object.id)
            data = {'status': task.status, 'task_id': task.id}
        elif 'download_status' in request.GET:
            if request.GET.get('task_id', ''):
                result = app.AsyncResult(request.GET['task_id'])
                data = {'status': result.status}
            else:
                data = {'status': 'FAILED'}

        return Response(data)
