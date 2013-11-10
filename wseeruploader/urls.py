import os
from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView

admin.autodiscover()

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
         return "/upload/new"
        # return "/upload/" + user.get_absolute_url()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/register/$',
    #    MyRegistrationView.as_view(), name='registration_register'),
	#url(r'^accounts/',
    #    include('wseeruploader.apps.registration.backends.simple.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^upload/', include('wseeruploader.apps.fileupload.urls',
        namespace="fileupload")),
)

urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'media')}),
)
