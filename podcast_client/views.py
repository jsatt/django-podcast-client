from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import PodcastChannel, PodcastItem


class ChannelList(ListView):
    model = PodcastChannel


class ChannelDetail(DetailView):
    model = PodcastChannel


class ItemDetail(DetailView):
    model = PodcastItem
