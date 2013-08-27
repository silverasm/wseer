from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
         return "/upload/new"
        # return "/upload/" + user.get_absolute_url()

urlpatterns = patterns('',
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^upload/', include('mysite.fileupload.urls')),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

import os
urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
)
