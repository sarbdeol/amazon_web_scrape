from django.contrib import admin
import os
# Register your models here.
from .models import Header

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Header._meta.fields]  # Display all fields in the admin list

from .models import ScrapedData

class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ('url', 'status')

admin.site.register(ScrapedData, ScrapedDataAdmin)
from .models import UploadedFile
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'uploaded_at']  # Customize the displayed fields as needed

    def get_existing_files(self):
        # Get a list of existing files in the 'media/upload' folder
        upload_directory = 'media/upload'
        existing_files = []
        if os.path.exists(upload_directory) and os.path.isdir(upload_directory):
            existing_files = os.listdir(upload_directory)
        return existing_files

    def get_queryset(self, request):
        # Retrieve all UploadedFile objects
        queryset = super().get_queryset(request)
        return queryset

    def changelist_view(self, request, extra_context=None):
        # Add existing files to the context to display in the admin interface
        extra_context = extra_context or {}
        extra_context['existing_files'] = self.get_existing_files()
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(UploadedFile, UploadedFileAdmin)

from .models import ScrapeDataCount

@admin.register(ScrapeDataCount)
class ScrapeDataCountAdmin(admin.ModelAdmin):
    list_display = ['count']