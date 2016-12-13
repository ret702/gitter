from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import render
from polls.controllers.process import processCommand
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.uploadedfile import UploadedFile
import tempfile



file=UploadedFile()
file_list=[]
def index(request):
    template = loader.get_template('polls/index.html')
    context={}
    return HttpResponse(template.render(context, request))


def console(request):

    if request.is_ajax():
        command = request.POST.get("command")
        return JsonResponse(process(command))
    if (request.method=='POST'):
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('myfile')
        global file_list
        for f in files:
            file_list.append(f.name)
            handle_uploaded_file(f)
    template = loader.get_template('polls/console.html')
    context={}
    return HttpResponse(template.render(context, request))



def process(data):
    return processCommand(data,file_list)


def handle_uploaded_file(f):
    file_path=tempfile.gettempdir()+"\\" +(f.name)
    with open(file_path, 'wb+') as destination:
        destination.write(f.read())




