import os
from django.conf.urls import patterns, include, url
from django.contrib import admin
from wseeruploader.apps.fileupload.forms import *
from wseeruploader.apps.fileupload.views import RegistrationView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

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
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

