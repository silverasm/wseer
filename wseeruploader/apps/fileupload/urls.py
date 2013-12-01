from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from wseeruploader.apps.fileupload import views

urlpatterns = patterns('',
    url(r'^projects/$', views.ProjectListAndCreate, name="projects"),
    (r'^projects/d/(?P<pk>\d+)$',
        login_required(views.ProjectDelete.as_view()), {}, 'project-delete'),
    (r'^projects/(?P<proj_key>\d+)/$',
        login_required(views.UploadedFileCreateView.as_view()), {},
        'upload-new'),
    (r'^projects/(?P<proj_key>\d+)/d/(?P<pk>\d+)$',
        login_required(views.UploadedFileDeleteView.as_view()), {},
        'upload-delete'),
    url(r'^annotate/(?P<pk>\d+)$', views.annotate, name='annotate'),
    url(r'^process/(?P<pk>\d+)$', views.process, name='process'),
)

