from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from wseeruploader.apps.fileupload.views import (UploadedFileCreateView,
    UploadedFileDeleteView, ProjectDelete)
from wseeruploader.apps.fileupload import views



urlpatterns = patterns('',
    url(r'^projects/$', views.ProjectListAndCreate, name="projects"),
    (r'^projects/d/(?P<pk>\d+)$', login_required(ProjectDelete.as_view()), {},
        'project-delete'),
    (r'^projects/(?P<proj_key>\d+)/$', login_required(UploadedFileCreateView.as_view()), {},
        'upload-new'),
    (r'^projects/(?P<proj_key>\d+)/d/(?P<pk>\d+)$',
        login_required(UploadedFileDeleteView.as_view()), {}, 'upload-delete'),
    url(r'^annotate/(?P<pk>\d+)$', views.annotate, name='annotate'),
    
)

