from .celery import app
from .models import PodcastChannel, PodcastItem


@app.task
def update_channel(slug, force_download=False):
    channel = PodcastChannel.objects.get(slug=slug)
    channel.update_channel(download=force_download)


@app.task
def update_all_channels(force_download=False):
    for channel in PodcastChannel.objects.all():
        channel.update_channel(download=force_download)


@app.task
def download_file(item_id):
    item = PodcastItem.objects.get(id=item_id)
    item.download_file()
