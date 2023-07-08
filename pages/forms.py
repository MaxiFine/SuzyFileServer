from django import forms
from .models import File



# Upload form
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'description', 'file',)


# Sending Email
class EmailFileForm(forms.Form):
    email = forms.EmailField(label="Email Address",required=True)
    subject = forms.CharField( max_length=50, required=True)
    message = forms.CharField( max_length=150, required=False)
        
