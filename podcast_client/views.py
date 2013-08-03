from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .api.serializers import (
    PodcastChannelDetailSerializer, PodcastChannelSerializer,
    PodcastItemDetailSerializer)
from .models import PodcastChannel, PodcastItem


class ChannelList(ListView):
    model = PodcastChannel


class ChannelDetail(DetailView):
    model = PodcastChannel


class ItemDetail(DetailView):
    model = PodcastItem


class ChannelListAPI(ListCreateAPIView):
    model = PodcastChannel
    serializer_class = PodcastChannelSerializer

    def post_save(self, obj, created):
        obj.update_channel()


class ChannelDetailAPI(RetrieveUpdateAPIView):
    model = PodcastChannel
    serializer_class = PodcastChannelDetailSerializer
    lookup_field = 'slug'


class ItemDetailAPI(RetrieveUpdateAPIView):
    model = PodcastItem
    serializer_class = PodcastItemDetailSerializer
    lookup_field = 'slug'
