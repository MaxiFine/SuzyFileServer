from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


    
def validate_image_file(value):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'mp3', 'mp4', 'mkv']
    ext = value.name.split('.')[-1].lower()
    if ext not in allowed_extensions:
        raise models.ValidationError("Only specific file types are allowed.")


class File(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='media/', validators=[validate_image_file])
    

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("file_detail", kwargs={"pk": self.pk})

