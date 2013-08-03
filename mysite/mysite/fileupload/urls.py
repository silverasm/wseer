from django.conf.urls import patterns, include, url
from mysite.fileupload.views import PictureCreateView, PictureDeleteView
from mysite.registration.backends.simple.views import RegistrationView
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login

from mysite.registration import signals
from mysite.registration.views import RegistrationView as BaseRegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        # return "/upload/new"
        return "/upload/" + user.get_absolute_url()

urlpatterns = patterns('',
	# (r"^(?P<username>\w+)/$", PictureCreateView.as_view(), {}, 'upload-new'),
	# (r'^/$'+user.get_absolute_url(),PictureCreateView.as_view(), {}, 'upload-new'),
    (r'^new/$', PictureCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
)

