from rest_framework import serializers

from podcast_client.models import PodcastChannel, PodcastItem


class PodcastChannelSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_channel_details', lookup_field='slug')

    class Meta:
        model = PodcastChannel
        fields = ('url', 'api_url', 'title', 'slug')
        read_only_fields = ('title', 'slug')


class PodcastItemSerializer(serializers.ModelSerializer):
    media_type = serializers.Field(source='media_type')
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_item_details', lookup_field='slug')

    class Meta:
        model = PodcastItem
        fields = ('url', 'api_url', 'title', 'slug', 'publish_date',
                  'media_type', 'listened')
        read_only_fields = ('url', 'title', 'slug', 'publish_date')


class PodcastChannelDetailSerializer(serializers.HyperlinkedModelSerializer):
    items = PodcastItemSerializer(source='podcast_items', read_only=True)

    class Meta:
        model = PodcastChannel
        fields = ('url', 'title', 'slug', 'description', 'website',
                  'copyright', 'cover_url', 'download_new', 'items')
        read_only_fields = ('title', 'slug', 'description', 'website',
                            'copyright', 'cover_url')


class PodcastItemDetailSerializer(serializers.ModelSerializer):
    media_type = serializers.Field(source='media_type')
    channel = PodcastChannelSerializer(read_only=True)

    class Meta:
        model = PodcastItem
        fields = (
            'channel', 'url', 'title', 'slug', 'description', 'author', 'link',
            'publish_date', 'media_type', 'listened', 'cover_url')
        read_only_fields = (
            'url', 'title', 'slug', 'description', 'author', 'link',
            'publish_date', 'cover_url')
