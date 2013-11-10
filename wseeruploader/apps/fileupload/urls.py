from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.urlresolvers import reverse

from wseeruploader.apps.fileupload.views import (UploadedFileCreateView,
    UploadedFileDeleteView, ProjectDelete)
from wseeruploader.apps.fileupload import views

#from registration.backends.simple.views import (
#    RegistrationView)
#from wseeruploader.apps.registration import signals
#from wseeruploader.apps.registration.views import (
#    RegistrationView as BaseRegistrationView)

#class MyRegistrationView(RegistrationView):
#    def get_success_url(self, request, user):
#        # return "/upload/new"
#        return "/upload/" + user.get_absolute_url()

urlpatterns = patterns('',
    url(r'^projects/$', views.ProjectListAndCreate, name="projects"),
    (r'^projects/d/(?P<pk>\d+)$', ProjectDelete.as_view(), {},
        'project-delete'),
    (r'^projects/(?P<proj_key>\d+)/$', UploadedFileCreateView.as_view(), {},
        'upload-new'),
    (r'^projects/(?P<proj_key>\d+)/d/(?P<pk>\d+)$',
        UploadedFileDeleteView.as_view(), {}, 'upload-delete'),
    url(r'^annotate/(?P<pk>\d+)$', views.annotate, name='annotate'),
    
)

