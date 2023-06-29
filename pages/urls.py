from django.urls import path
from .views import (about, home, feeds_page,
                    file_preview, file_download, file_upload,)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('feeds/', feeds_page, name='feed'),
    path('file/<int:file_id>/preview/', file_preview, name='file_preview'),
    path('file/<int:file_id>/download/', file_download, name='file_download'),
    path('file/upload/', file_upload, name='uploads'),
]

