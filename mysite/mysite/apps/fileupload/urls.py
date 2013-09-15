from django.conf.urls import patterns, include, url
from mysite.apps.fileupload.views import (UploadedFileCreateView,
    UploadedFileDeleteView)
from mysite.apps.registration.backends.simple.views import RegistrationView
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login

from mysite.apps.registration import signals
from mysite.apps.registration.views import RegistrationView as BaseRegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        # return "/upload/new"
        return "/upload/" + user.get_absolute_url()

urlpatterns = patterns('',
	# (r"^(?P<username>\w+)/$", PictureCreateView.as_view(), {}, 'upload-new'),
	# (r'^/$'+user.get_absolute_url(),PictureCreateView.as_view(), {}, 'upload-new'),
    (r'^new/$', UploadedFileCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<pk>\d+)$', UploadedFileDeleteView.as_view(), {},
        'upload-delete'),
    #(r'^annotate/(?P<pk>\d+)$', FileAnnotate.as_view(), {}, 'upload-annotate')
)

