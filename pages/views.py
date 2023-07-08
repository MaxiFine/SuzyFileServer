from django.views.generic import ListView
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from .models import File
from .forms import FileUploadForm, EmailFileForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

@login_required
def feeds_page(request):
    files = File.objects.all()
    paginator = Paginator(files, per_page=6) 

    page_number = request.GET.get('page')
    try:
        files = paginator.get_page(page_number)  
    except PageNotAnInteger:
        files = paginator.get_page(1) 
    except EmptyPage:
        files = paginator.get_page(paginator.num_pages)
        
    return render(request, 'feeds.html', {"files":files})

@login_required
def file_detail_view(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, 'file_detail.html', {'file': file}) 

@login_required
def file_download(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.downloads += 1
    file.save()
    return redirect(file.file.url)

@staff_member_required
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


@login_required
def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = File.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
    context_data = {
        'query': query,
        'files': results
    }
    return render(request, 'search_.html', context_data)

@login_required
def send_email(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if request.method == 'POST':
        form = EmailFileForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', '')
            subject = form.cleaned_data.get('subject', '')
            message = form.cleaned_data.get('message', '')
        email = EmailMessage(
                subject,
                message,
                request.user.email,
                [email,],
        )
        # Attach file to the email
        email.attach_file(file.file.path)
        email.send()
    
        # Update count of emails sent
        file.emails_sent += 1
        file.save()
        messages.success(request=request, message=f'"{file.title}" successfully emailed')
        return redirect('file_detail', file_id)
    else:
        form = EmailFileForm()
    
    return render(request, 'email_file.html', {'form':form, 'file':file})
