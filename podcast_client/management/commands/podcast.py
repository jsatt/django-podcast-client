from optparse import make_option

from django.core.management.base import BaseCommand
from requests.exceptions import RequestException

from podcast_client.models import PodcastChannel


class Command(BaseCommand):
    args = '<arg1> <arg2> ...'
    help = 'Command line utility for managing podcasts in '
    'django-podcast-client'
    option_list = BaseCommand.option_list + (
        make_option('-l', '--list', action='store_true', dest='list',
                    help='List all podcasts currently subscribed'),
        make_option('-s', '--subscribe', action='store_true', dest='subscribe',
                    help='Subcribe to podcasts'),
        make_option('-u', '--update', action='store_true', dest='update',
                    help='Update podcasts'),
        make_option('-d', '--download', action='store_true', dest='download',
                    help='Download new items when updating'),
        make_option('--unsubscribe', action='store_true',
                    dest='unsubscribe',
                    help='Unsubscribe podcast and \033[4mdelete\033[0m '
                    'associated files'),
    )

    def handle(self, *args, **options):
        if options.get('subscribe'):
            self.subscribe(*args, **options)
        elif options.get('update'):
            self.update(*args, **options)
        elif options.get('list'):
            self.list(*args, **options)
        elif options.get('unsubscribe'):
            self.unsubscribe(*args, **options)

    def unsubscribe(self, *args, **options):
        try:
            channel = PodcastChannel.objects.get(slug=args[0])
        except (IndexError, PodcastChannel.DoesNotExist):
            self.stderr.write('Please enter a valid slug. Use -l or --list to '
                              'see all available slugs.')
        else:
            name = unicode(channel)
            channel.delete()
            self.stdout.write('"%s" unsubscribed and deleted.' % name)

    def list(self, *args, **options):
        for channel in PodcastChannel.objects.all():
            self.stdout.write('%s (%s)' % (channel.title, channel.slug))

    def subscribe(self, *args, **options):
        for url in args:
            try:
                PodcastChannel.subscribe(url)
            except RequestException:
                self.stderr.write('"%s" is not a valid url. Skipping.' % url)

    def update(self, *args, **options):
        if not args:
            channels = PodcastChannel.objects.all()
        else:
            channels = PodcastChannel.objects.filter(slug__in=args)

        if channels:
            for channel in channels:
               channel.update_channel(download=options['download'])
        else:
            self.stderr.write('Please enter at least one valid slug or no '
                              'slugs to update all. Use -l or --list to '
                              'see all available slugs.')
