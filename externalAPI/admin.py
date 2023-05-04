from django.contrib import admin

from .models import Publication


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'manager', 'title', 'addingDate', 'numberOfDownloads', 'isAvailable')
    list_filter = ('manager', 'isAvailable')
    search_fields = ('title', 'body', 'manager__username')

admin.site.register(Publication, PublicationAdmin)



