from wseeruploader.apps.fileupload.models import UploadedFile
from django.views.generic import CreateView, DeleteView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings
from django.shortcuts import render, get_object_or_404

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class UploadedFileCreateView(CreateView):
    model = UploadedFile

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + "files/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(UploadedFileCreateView, self).get_context_data(**kwargs)
        context['files'] = UploadedFile.objects.all()
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

def annotate(request, pk):
    f = get_object_or_404(UploadedFile, pk=pk)
    context = {"file": f}
    return render(request, "fileupload/uploadedfile_annotate.html", context)

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
