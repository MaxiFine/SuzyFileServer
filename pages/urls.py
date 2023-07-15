from django.urls import path
from .views import (about, home, feeds_page, file_download, file_upload,
                    search_view, send_email, file_detail_view)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('feeds/', feeds_page, name='feed'),
    path('file/<int:file_id>/download/', file_download, name='file_download'),
    path('file/upload/', file_upload, name='uploads'),
    path("search/", search_view, name="search_results"), 
    path('file/<int:file_id>/detail/', file_detail_view, name='file_detail'),
    path('send_email/<int:file_id>/', send_email, name='emails'),
    
]

