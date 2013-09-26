from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login

from wseeruploader.apps.fileupload.views import (UploadedFileCreateView,
    UploadedFileDeleteView, ProjectListView)
from wseeruploader.apps.registration.backends.simple.views import (
    RegistrationView)
from wseeruploader.apps.fileupload import views
from wseeruploader.apps.registration import signals
from wseeruploader.apps.registration.views import (
    RegistrationView as BaseRegistrationView)

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        # return "/upload/new"
        return "/upload/" + user.get_absolute_url()

urlpatterns = patterns('',
    url(r'^projects/$', ProjectListView.as_view(), name="project-list"),
    (r'^projects/files/$', UploadedFileCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<pk>\d+)$', UploadedFileDeleteView.as_view(), {},
        'upload-delete'),
    url(r'^annotate/(?P<pk>\d+)$', views.annotate, name='annotate'),
    
)

