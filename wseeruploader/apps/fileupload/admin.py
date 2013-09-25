from django.contrib import admin
from wseeruploader.apps.fileupload.models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['slug']}),
        ('File info', {'fields': ['file', 'status']}),
    ]
    list_display = ('slug', 'file', 'status')
    list_filter = ['status']

admin.site.register(UploadedFile, UploadedFileAdmin)

