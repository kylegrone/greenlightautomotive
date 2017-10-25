from django.forms import ModelForm
from django import forms
from livechat.models import Upload


# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload
        pic_attr = {
                      'class':"upload_pic_button"
                      
                      }
        widgets={
                  "pic":forms.FileInput(attrs=pic_attr),
                  
                } 
        fields = ["pic"]