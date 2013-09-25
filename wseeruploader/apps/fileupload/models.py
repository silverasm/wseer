from django.db import models
from django.conf import settings
import os

class UploadedFile(models.Model):
    STATE_UPLOADED = 0
    STATE_ANNOTATED = 1
    STATE_PROCESSING = 2
    STATE_PROCESSED = 4
    STATES = (
        (STATE_UPLOADED, "Uploaded"),
        (STATE_ANNOTATED, "Annotated"),
        (STATE_PROCESSING, "Processing"),
        (STATE_PROCESSED, "Processed"),
    )

    status = models.SmallIntegerField(choices=STATES,
        default=0, blank=True, null=True) 
    file = models.FileField(upload_to=settings.XML_ROOT)

    def __unicode__(self):
        return self.file.name

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('upload-new', )

    def name(self):
        return os.path.basename(self.file.name)
    
    def save(self, *args, **kwargs):
        if not self.status:
            self.status = self.STATE_UPLOADED
        super(UploadedFile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        self.file.delete(False)
        super(UploadedFile, self).delete(*args, **kwargs)
