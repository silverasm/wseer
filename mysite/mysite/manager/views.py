from django.http import HttpResponse

def newProject(request):
	return HttpResponseRedirect("/upload/new/")


