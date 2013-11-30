import os
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView as SimpleRegistrationView
from wseeruploader.apps.fileupload.forms import *
from django.contrib.auth import views as auth_views


#Override regular registration view so it redirects where we want it
class RegistrationView(SimpleRegistrationView):
    form_class = BootstrapRegistrationForm
    def get_success_url(self, request, user):
        return (settings.LOGIN_REDIRECT_URL, (), {})

admin.autodiscover()

authpatterns = patterns('',
    url(r'^register/$',
        RegistrationView.as_view(),
        name='registration_register'),
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'registration/login.html',
            'authentication_form': BootstrapAuthenticationForm},
        name='auth_login'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'password_change_form': BootstrapPasswordChangeForm},
        name='auth_password_change'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'password_reset_form': BootstrapPasswordResetForm},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'authentication_form': BootstrapSetPasswordForm},
        name='auth_password_reset_confirm'),
    (r'^', include('registration.backends.simple.urls')),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/', include('wseeruploader.apps.fileupload.urls',
        namespace="fileupload")),
    url(r'^accounts/', include(authpatterns)),
    #url(r'^login/', include('social.apps.django_app.urls', namespace='social')),
)

urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'media')}),
)
