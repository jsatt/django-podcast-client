from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .api.serializers import (
    PodcastChannelDetailSerializer, PodcastItemDetailSerializer)
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
