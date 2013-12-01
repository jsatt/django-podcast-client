from rest_framework import pagination, serializers

from podcast_client.models import PodcastChannel, PodcastItem


class DetailPaginationSerializer(pagination.PaginationSerializer):
    per_page = serializers.Field(source='paginator.per_page')
    page_count = serializers.Field(source='paginator.num_pages')


class PodcastChannelDetailSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_channel_details', lookup_field='slug')
    items_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_channel_items', lookup_field='slug')
    has_unlistened = serializers.Field(source='has_unlistened')
    latest_publish_date = serializers.SerializerMethodField(
        'get_latest_publish_date')

    class Meta:
        model = PodcastChannel
        fields = ('url', 'api_url', 'items_url', 'title', 'slug',
                  'description', 'website', 'copyright', 'cover_url',
                  'download_new', 'has_unlistened')
        read_only_fields = ('title', 'slug', 'description', 'website',
                            'copyright', 'cover_url')

    def get_latest_publish_date(self, obj):
        return obj.podcast_items.latest().publish_date


class PodcastItemDetailSerializer(serializers.HyperlinkedModelSerializer):
    media_type = serializers.Field(source='media_type')
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_item_details', lookup_field='slug')
    channel_url = serializers.HyperlinkedRelatedField(
        source='channel', view_name='podcast_client:api_channel_details',
        lookup_field='slug', read_only=True)
    file_downloaded = serializers.SerializerMethodField(
        'is_file_downloaded')

    class Meta:
        model = PodcastItem
        fields = (
            'url', 'api_url', 'channel_url', 'title', 'slug', 'description',
            'author', 'link', 'publish_date', 'media_type', 'listened',
            'cover_url', 'file_downloaded')
        read_only_fields = (
            'url', 'title', 'slug', 'description', 'author', 'link',
            'publish_date', 'cover_url')

    def is_file_downloaded(self, obj):
        return bool(obj and obj.file)
