import os
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView as SimpleRegistrationView

#Override regular registration view so it redirects where we want it
class RegistrationView(SimpleRegistrationView):
    def get_success_url(self, request, user):
        return (settings.LOGIN_REDIRECT_URL, (), {})

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/', include('wseeruploader.apps.fileupload.urls',
        namespace="fileupload")),
    url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),

    #url(r'^login/', include('social.apps.django_app.urls', namespace='social')),
)

urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'media')}),
)
