import mimetypes  # for checking file types
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse



class File(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='media/')
    downloads = models.PositiveIntegerField(default=0)
    emails_sent = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def get_file_type(self):
        file_path = self.file.path
        file_type, _ = mimetypes.guess_type(file_path)
        if file_type:
            return file_type.split('/')[0]
            
    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("file_detail", kwargs={"pk": self.pk})

