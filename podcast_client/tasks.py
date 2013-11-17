from podcast_client.models import PodcastChannel, PodcastItem


def update_channel(slug, force_download=False):
    channel = PodcastChannel.objects.get(slug=slug)
    channel.update_channel(download=force_download)


def update_all_channels(force_download=False):
    for channel in PodcastChannel.objects.all():
        channel.update_channel(download=force_download)


def download_file(item_id):
    item = PodcastItem.objects.get(id=item_id)
    item.download_file()

try:
    from .celery import app
except ImportError:
    pass
else:
    update_channel = app.task(update_channel)
    update_all_channels = app.task(update_all_channels)
    download_file = app.task(download_file)
