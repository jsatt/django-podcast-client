from rest_framework import pagination, serializers

from podcast_client.models import PodcastChannel, PodcastItem


class PodcastChannelSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_channel_details', lookup_field='slug')
    has_unlistened = serializers.Field(source='has_unlistened')
    latest_publish_date = serializers.SerializerMethodField(
        'get_latest_publish_date')

    class Meta:
        model = PodcastChannel
        fields = ('url', 'api_url', 'title', 'slug', 'has_unlistened',
                  'latest_publish_date', 'cover_url')
        read_only_fields = ('title', 'slug')

    def get_latest_publish_date(self, obj):
        return obj.podcast_items.latest().publish_date


class PodcastItemSerializer(serializers.ModelSerializer):
    media_type = serializers.Field(source='media_type')
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_item_details', lookup_field='slug')
    file_downloaded = serializers.SerializerMethodField(
        'is_file_downloaded')

    class Meta:
        model = PodcastItem
        fields = ('url', 'api_url', 'title', 'slug', 'publish_date',
                  'media_type', 'listened', 'file_downloaded')
        read_only_fields = ('url', 'title', 'slug', 'publish_date')

    def is_file_downloaded(self, obj):
        return bool(obj and obj.file)


class DetailPaginationSerializer(pagination.PaginationSerializer):
    per_page = serializers.Field(source='paginator.per_page')
    page_count = serializers.Field(source='paginator.num_pages')


class PodcastChannelDetailSerializer(serializers.HyperlinkedModelSerializer):
    items = PodcastItemSerializer(source='podcast_items', read_only=True)
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_channel_details', lookup_field='slug')
    has_unlistened = serializers.Field(source='has_unlistened')
    latest_publish_date = serializers.SerializerMethodField(
        'get_latest_publish_date')

    class Meta:
        model = PodcastChannel
        fields = ('url', 'api_url', 'title', 'slug', 'description', 'website',
                  'copyright', 'cover_url', 'download_new', 'items',
                  'has_unlistened')
        read_only_fields = ('title', 'slug', 'description', 'website',
                            'copyright', 'cover_url')

    def get_latest_publish_date(self, obj):
        return obj.podcast_items.latest().publish_date


class PodcastItemDetailSerializer(serializers.ModelSerializer):
    media_type = serializers.Field(source='media_type')
    channel = PodcastChannelSerializer(read_only=True)
    api_url = serializers.HyperlinkedIdentityField(
        view_name='podcast_client:api_item_details', lookup_field='slug')
    file_downloaded = serializers.SerializerMethodField(
        'is_file_downloaded')

    class Meta:
        model = PodcastItem
        fields = (
            'channel', 'url', 'api_url', 'title', 'slug', 'description',
            'author', 'link', 'publish_date', 'media_type', 'listened',
            'cover_url', 'file_downloaded')
        read_only_fields = (
            'url', 'title', 'slug', 'description', 'author', 'link',
            'publish_date', 'cover_url')

    def is_file_downloaded(self, obj):
        return bool(obj and obj.file)
