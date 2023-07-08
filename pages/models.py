from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse



class File(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='media/')
    

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("file_detail", kwargs={"pk": self.pk})

