from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from . import views


api_patterns = patterns(
    '',
    url(r'^channels$', views.ChannelListAPI.as_view(), name='api_channels'),
    url(r'^channels/(?P<slug>[a-zA-Z\d\-\_]+)$',
        views.ChannelDetailAPI.as_view(), name='api_channel_details'),
    url(r'^channels/(?P<slug>[a-zA-Z\d\-\_]+)/items$',
        views.ItemListAPI.as_view(), name='api_channel_items'),
    url(r'^items/(?P<slug>[a-zA-Z\d\-\_]+)$', views.ItemDetailAPI.as_view(),
        name='api_item_details'),
    url(r'^items/(?P<slug>[a-zA-Z\d\-\_]+)/file$',
        views.ItemFileAPI.as_view(), name='api_item_file'),
)

urlpatterns = patterns(
    '',
    url(r'^api/', include(api_patterns)),
    url(r'^$', TemplateView.as_view(template_name='podcast_client/home.html'),
        name='home'),
)
