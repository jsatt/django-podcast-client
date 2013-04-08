from podcast_client.models import PodcastChannel


def update_channel(slug, force_download=False):
    channel = PodcastChannel.objects.get(slug=slug)
    channel.update_channel(download=force_download)


def update_all_channels(force_download=False):
    for channel in PodcastChannel.objects.all():
        channel.update_channel(download=force_download)

try:
    from celery.decorators import task
except ImportError:
    pass
else:
    update_channel = task(update_channel)
    update_all_channels = task(update_all_channels)
