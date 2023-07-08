from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import File
from .forms import FileUploadForm, EmailFileForm


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


# Done with the feeds, uploads and downloads
# next is now search and then previews then 
# emails sending and then checking all downloads
# and the downloads of each file

class SearchResultsListView(ListView): 
    model = File
    context_object_name = "searches"
    template_name = "search_.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return File.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query))
    

# def send_email(request, pk):
#     file = get_object_or_404(File, pk=pk)
#     if request.method == 'POST':
#         form = EmailFileForm(request.POST, request.FILES,)
#         if form.is_valid():
#             recipient_email = form.cleaned_data['recipient_email']
#             subject = form.cleaned_data['subject']
            
#             email = EmailMessage(
#                 subject,
#                 'Please consider the attached file',
#                 'gibboel5@gmail.com',
#                 [recipient_email],
#             )
#             email.attach_file(file.file.path)
#             email.send()

#             # Count email sent
#             file.emails_sent += 1
#             file.save()

#             messages.success(request, 'File Sent')
#             return redirect('feed')
#     else:
#         form = EmailFileForm()
    
#     return render(request, 'email_file.html', {'form': form})


def send_email(request, file_id):
    file = get_object_or_404(File, id=file_id)
    sent = False
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        
        email = EmailMessage(
                'File Email',
                'Please consider the attached file',
                'gibboel5@gmail.com',
                [recipient_email],
        )
        # Attach file to the email
        email.attach_file(file.file.path)
        email.send()
    
        # Update count of emails sent
        file.emails_sent += 1
        file.save()
        messages.success(request=request, message='File Emailed')
        sent = True
        return redirect('feed')
    
