from django.contrib import admin

from .models import PodcastChannel, PodcastItem


class PodcastChannelAdmin(admin.ModelAdmin):
    actions = ('update_channels',)
    list_display = ('title', 'download_new',)
    readonly_fields = ('title', 'description', 'slug', 'cover', 'cover_url',
                       'created', 'modified')
    search_fields = ('title',)

    def update_channels(self, request, queryset):
        for channel in queryset:
            channel.update_channel()


class PodcastItemAdmin(admin.ModelAdmin):
    actions = ('download_files', 'delete_files',)
    list_display = ('title', 'channel', 'publish_date', 'file', 'listened')
    list_filter = ('channel', )
    readonly_fields = ('title', 'channel', 'url', 'file', 'file_type',
                       'description', 'publish_date', 'guid')
    search_fields = ('title',)
    
    def download_files(self, request, queryset):
        for item in queryset:
            item.download_file()

    def delete_files(self, request, queryset):
        for item in queryset:
            item.delete_file()
        

admin.site.register(PodcastChannel, PodcastChannelAdmin)
admin.site.register(PodcastItem, PodcastItemAdmin)
