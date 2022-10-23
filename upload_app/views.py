from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect)
from django.urls import reverse_lazy
from .forms import (
    UploadFileForm,
    UploadFileFormCustom
)
from django.views.generic import DetailView
from .models import UploadFile
from django.core.files.base import ContentFile
from django.views.generic import TemplateView


# Create your views here.
def uploadFile(request):
    # return HttpResponse('Hello world')
    UF = UploadFileForm
    return render(request, 'upload_app/fileupload.html', {'UF': UF})
    # return getFile(request)


# Using model form
def getFile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            obj = form.save()
            # return HttpResponseRedirect('/success/url/')
            return HttpResponse('Save file success')
            # return HttpResponseRedirect(reverse_lazy('upload:getfile', kwargs={'pk': obj.id}))
    else:
        form = UploadFileForm
    return render(request, 'upload_app/fileupload.html', {'UF': form})


def handle_uploaded_file(f):
    with open('media/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# Using form custom
def uploadFileCustom(request):
    UF = UploadFileFormCustom
    return render(request, 'upload_app/fileupload_custom.html', {'UF': UF})


def getFileCustom(request):
    if request.method == 'POST':
        form = UploadFileFormCustom(request.POST, request.FILES)
        if form.is_valid():
            # content_file = ContentFile(b'Hello world!', name='filename.txt')
            # file_field = content_file
            instance = UploadFile(image=request.FILES['image_form'], title = form.cleaned_data['title_form'] ) #là FILES['image'] form
            instance.save()
            # print(obj.id)
            # return HttpResponseRedirect('/success/url/')
            return HttpResponse('Save file success')
            # return HttpResponseRedirect(reverse_lazy('upload:view_upload_customform_page', kwargs={'pk': obj.id}))
    else:
        form = UploadFileFormCustom()
    return render(request, 'upload_app/fileupload_custom.html', {'UF': form})


def uploadFileCustomForm_view(request):
    UF = UploadFileFormCustom
    return render(request, 'upload_app/fileupload_custom_display.html', {'UF': UF})


# Upload template
class UploadImageDisplay(DetailView):
    model = UploadFile
    template_name = 'upload_app/upload_image_display.html'
    context_object_name = 'UF'


class UploadImage(TemplateView):
    form = UploadFileForm
    template_name = 'upload_app/upload_image.html'

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('upload:view_upload_template_page', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)