from django.db import models
from django.conf import settings
import os

class UploadedFile(models.Model):
    # We use slugs to store the filename for easy access.

    STATES = (
        (0, "Uploaded"),
        (1, "Annotated"),
        (2, "Processing"),
        (4, "Processed"),
    )

    status = models.SmallIntegerField(choices=STATES,
        default=0, blank=True, null=True) 
    file = models.FileField(upload_to=settings.XML_ROOT)
    name = models.FilePathField(path=settings.MEDIA_ROOT, blank=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.name = self.file.name
        super(UploadedFile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        self.file.delete(False)
        super(UploadedFile, self).delete(*args, **kwargs)
