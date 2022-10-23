from .models import UploadFile
from django import forms

class UploadFileForm(forms.ModelForm):
    # Nếu Form dùng chung với models
    class Meta:
        model = UploadFile
        fields = ['title', 'image', 'body']

class UploadFileFormCustom(forms.Form):
    title_form = forms.CharField(max_length=255)
    image_form = forms.ImageField()
    body_form = forms.CharField(widget=forms.Textarea)

    # Nếu Form dùng chung với models
    # class Meta:
    #     model = UploadFile
    #     fields = ['title', 'image']