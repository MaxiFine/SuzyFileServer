from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import File


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def feeds_page(request):
    files = File.objects.all()
    return render(request, 'feeds_page.html', {'files': files})


def file_preview(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, 'file_preview.html', {'file': file}) 


def file_download(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    return response

def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.save()
            return redirect('feed')
    else:
        form = FileUploadForm()
    return render(request, 'file_upload.html', {'form': form})