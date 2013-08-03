from django.conf.urls import include, patterns, url

from . import views


api_patterns = patterns(
    '',
    url(r'^channels$', views.ChannelListAPI.as_view(), name='api_channels'),
    url(r'^channels/(?P<slug>[a-zA-Z\d\-\_]+)$',
        views.ChannelDetailAPI.as_view(), name='api_channel_details'),
    url(r'^items/(?P<slug>[a-zA-Z\d\-\_]+)$', views.ItemDetailAPI.as_view(),
        name='api_item_details'),
)

urlpatterns = patterns(
    '',
    url(r'^$', views.ChannelList.as_view(), name='home'),
    url(r'^api/', include(api_patterns)),
    url(r'^channels/$', views.ChannelList.as_view(), name='channel_list'),
    url(r'^channels/(?P<slug>[a-zA-Z\d\-]+)/$', views.ChannelDetail.as_view(),
        name='channel_detail'),
    url(r'^channels/(?P<channel_slug>[a-zA-Z\d\-]+)/(?P<pk>\d+)/$',
        views.ItemDetail.as_view(), name='item_detail'),
)
