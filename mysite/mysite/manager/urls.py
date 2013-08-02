from django.conf.urls import include, patterns, url
from django.views.generic.base import TemplateView
from views import *


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='main.html')),

)
