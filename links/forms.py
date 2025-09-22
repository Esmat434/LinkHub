from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import (
    Link
)

class LinkFormCreation(forms.ModelForm):
    class Meta:
        model = Link
        fields =  (
            'title','url','icon','status'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
            'url': forms.URLInput(attrs={'class':'form-control','placeholder':'Enter Url'}),
            'icon': forms.FileInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control', 'placeholder':'Select Status'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title',None)

        if not title:
            raise forms.ValidationError("Please Enter The Title.")
        
        if Link.objects.filter(title=title, user=self.user).exists():
            raise forms.ValidationError("This Title Already Exists.")
        
        return title
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        validator = URLValidator()
        try:
            validator(url)
        except ValidationError:
            raise forms.ValidationError("Enter a valid URL.")
        return url

    def save(self, commit = True):
        link = super().save(commit=False)
        if self.user:
            link.user = self.user
        if commit:
            link.save()
        return link
    
class LinkFormUpdate(forms.ModelForm):
    class Meta:
        model = Link
        fields = (
            'title','url','icon','status'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
            'url': forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Url'}),
            'icon': forms.FileInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control', 'placeholder':'Select Status'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']

        if Link.objects.filter(title=title, user=self.user).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError("This Title Already Exists.")
        
        return title
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        validator = URLValidator()
        try:
            validator(url)
        except ValidationError:
            raise forms.ValidationError("Enter a valid URL.")
        return url
    
    def save(self, commit = True):
        link = super().save(commit=False)
        if self.user:
            link.user = self.user
        if commit:
            link.save()
        return link