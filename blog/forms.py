from django import forms
from blog.models import comment
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

class commentForm(forms.ModelForm):
    class Meta:
        model=comment
        fields=('name','email','body')
        
    