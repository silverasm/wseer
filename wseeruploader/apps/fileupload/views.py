from wseeruploader.apps.fileupload.models import UploadedFile, Project, ProjectForm, UploadedFileForm
from django.views.generic import CreateView, DeleteView, ListView, View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin

from django.conf import settings
from django.shortcuts import render, get_object_or_404

import logging
logger = logging.getLogger("apps.fileupload")

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class UploadedFileCreateView(CreateView):
    model = UploadedFile
    form_class = UploadedFileForm
    
    def form_valid(self, form):
        logger.debug("*********Inside form_valid")
        
        self.object = form.save(commit=False)
        self.object.project_id = self.kwargs['proj_key']
        self.object.save()
        logger.debug("ID1")
        logger.debug(self.object.name())
        logger.debug("/uploads/xmlfiles/" + self.object.name().replace(" ", "_"))
        logger.debug("ID2")
        f = self.request.FILES.get('file')
        
        data = [{
            'name': self.object.name(),
            'url': "/uploads/xmlfiles/" + self.object.name().replace(" ", "_"),
            'delete_url': reverse('fileupload:upload-delete',
                kwargs={'pk':self.object.id,
                'proj_key':self.kwargs['proj_key']}),
            'delete_type': "DELETE"}]
        
        response = JSONResponse(data, {}, response_mimetype(self.request))
        
        response['Content-Disposition'] = 'inline; filename=files.json'
        
        return super(UploadedFileCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        logger.debug("--KWARGS--")
        logger.debug(kwargs)
        logger.debug("--SELF KWARGS proj_key--")
        logger.debug(self.kwargs["proj_key"])
        logger.debug("--MODEL--")
        logger.debug(dir(self.model.project))
        context = super(UploadedFileCreateView, self).get_context_data(**kwargs)
        context['files'] = UploadedFile.objects.all()
        context['proj'] = int(self.kwargs["proj_key"])
        logger.debug("--CONTEXT--")
        logger.debug(context['proj'])
        return context


class UploadedFileDeleteView(DeleteView):
    model = UploadedFile

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect('/upload/new')

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
        return HttpResponseRedirect(reverse("projects"))

def annotate(request, pk):
    f = get_object_or_404(UploadedFile, pk=pk)
    context = {"file": f}
    return render(request, "fileupload/uploadedfile_annotate.html", context)

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
