from django import forms
from .models import File



# Upload form
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'description', 'file',)

