from django.views.generic import CreateView, DeleteView, ListView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registration.backends.simple.views import RegistrationView as SimpleRegistrationView
from wseeruploader.apps.fileupload.models import UploadedFile, Project
from wseeruploader.apps.fileupload.forms import ProjectForm, UploadedFileForm, BootstrapRegistrationForm
import json

import logging
logger = logging.getLogger("apps.fileupload")

# Javascript views

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

def render_to_json_response(self, context, **response_kwargs):
    data = json.dumps(context)
    return HttpResponse(data, **response_kwargs)

class JSONResponse(HttpResponse):
    """JSON response class."""
    
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        a = super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

# UploadedFile views

class UploadedFileCreateView(CreateView):
    model = UploadedFile
    form_class = UploadedFileForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project_id = self.kwargs['proj_key']
        self.object.save()
        f = self.request.FILES.get('file')

        data = [{
            'name': self.object.name(),
            'url': "/uploads/xmlfiles/" + self.object.name().replace(" ", "_"),
            'type': "application/xml",
            'size': self.object.file.size,
            'delete_url': reverse('fileupload:upload-delete',
                kwargs={'pk':self.object.id,
            'proj_key':self.kwargs['proj_key']}),
            'delete_type': "DELETE"}]

        return HttpResponse(simplejson.dumps(data),
            content_type=response_mimetype(self.request))

    def get_context_data(self, **kwargs):
        context = super(UploadedFileCreateView, self).get_context_data(**kwargs)
        context['files'] = UploadedFile.objects.all()
        context['proj'] = int(self.kwargs["proj_key"])
        return context

class UploadedFileDeleteView(DeleteView):
    model = UploadedFile

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        proj = self.kwargs["proj_key"]
        
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            logger.debug(proj)
            return HttpResponseRedirect(reverse("fileupload:upload-new",
                kwargs={'proj_key':proj}))

@login_required
def annotate(request, pk):
    f = get_object_or_404(UploadedFile, pk=pk)
    context = {"file": f}
    if f.status is f.STATE_UPLOADED:
        return render(request, "fileupload/uploadedfile_annotate.html", context)
    else:
        return render(request, "fileupload/uploadedfile_process.html", context)

# Project views

@login_required
def ProjectListAndCreate(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST':
        form.save()

    # notice this comes after saving the form to pick up new objects
    projects = Project.objects.all()
    return render(request, 'fileupload/projects.html',
        {'projects': projects, 'form': form})

class ProjectDelete(DeleteView):
    model = Project

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        for upfile in self.object.uploadedfile_set.all():
            upfile.delete()
        self.object.delete()
        return HttpResponseRedirect(reverse("fileupload:projects"))

# View to make sure redirects from registration work out okay

class RegistrationView(SimpleRegistrationView):
    form_class = BootstrapRegistrationForm
    def get_success_url(self, request, user):
        return (settings.LOGIN_REDIRECT_URL, (), {})