from django.contrib import admin

from podcast_client.models import PodcastChannel, PodcastItem


class PodcastChannelAdmin(admin.ModelAdmin):
    actions = ('update_channels',)
    list_display = ('title', 'download_new',)
    readonly_fields = ('title', 'description', 'slug', 'cover_url', 'created',
                       'modified')
    search_fields = ('title',)

    def update_channels(self, request, queryset):
        for channel in queryset:
            channel.update_channel()

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.update_channel()


class PodcastItemAdmin(admin.ModelAdmin):
    actions = ('download_files', 'delete_files', 'mark_as_listened')
    list_editable = ('listened',)
    list_display = ('title', 'channel', 'publish_date', 'file', 'listened')
    list_filter = ('channel', 'listened')
    ordering = ('-publish_date',)
    readonly_fields = ('title', 'channel', 'url', 'file', 'file_type',
                       'description', 'publish_date', 'guid')
    search_fields = ('title', 'description')

    def download_files(self, request, queryset):
        for item in queryset:
            item.download_file()

    def delete_files(self, request, queryset):
        for item in queryset:
            item.delete_file()

    def mark_as_listened(self, request, queryset):
        queryset.update(listened=True)


admin.site.register(PodcastChannel, PodcastChannelAdmin)
admin.site.register(PodcastItem, PodcastItemAdmin)
