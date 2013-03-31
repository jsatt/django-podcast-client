from django.conf.urls import patterns, url

from .views import ChannelDetail, ChannelList, ItemDetail


urlpatterns = patterns('',
     url(r'^$', ChannelList.as_view(), name='home'),
     url(r'^channels/$', ChannelList.as_view(), name='channel_list'),
     url(r'^channels/(?P<slug>[a-zA-Z\d\-]+)/$', ChannelDetail.as_view(), name='channel_detail'),
     url(r'^channels/(?P<channel_slug>[a-zA-Z\d\-]+)/(?P<pk>\d+)/$', ItemDetail.as_view(), name='item_detail'),
)
