from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import File
from .forms import FileUploadForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def feeds_page(request):
    files = File.objects.all()
    return render(request, 'feeds.html', {'files': files})

@login_required
def file_preview(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, 'feeds_preview.html', {'file': file}) 

@login_required
def file_download(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    return response

@login_required
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


# # file upload view
# @login_required
# def file_upload(request):
#     if request.method == 'POST' and request.FILES:
#         uploaded_file = request.FILES
#         file = File(file=uploaded_file)
#         file.save()
#         return redirect("feed")
#     else:
#         form = FileUploadForm()
#     return render(request, 'file_upload.html', {'form': form})

