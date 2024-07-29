# django imports
from django import forms

#local imports
from .models import Post,Ad,Category,Tags


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields="__all__"
        exclude = ['author']

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields="__all__"
        
