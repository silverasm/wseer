from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.core.urlresolvers import reverse
import os

class Project(models.Model):
    """This is a project that is owned by a user and contains many
    UploadedFiles."""
    name = models.CharField(max_length=200)

    #def get_absolute_url(self):
    #    return reverse("projects")

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']

class UploadedFile(models.Model):
    """This represents a file that has been uploaded to the server."""
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
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.file.name

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

    def get_absolute_url(self):
        return u'/upload/projects/%d' % self.id 
    
class UploadedFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        exclude = ('project',)