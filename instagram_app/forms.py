from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import  Image, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, label='',widget=forms.EmailInput(attrs={'class': 'form-control mb-4', 'placeholder': 'email'}))
    username =forms.CharField(max_length=200, label='',widget=forms.TextInput(attrs={'class': 'form-control mb-4','placeholder': 'username'}))
    password1 = forms.CharField(max_length=200,label='',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder': 'password'}))
    password2 = forms.CharField(max_length=200, label='',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4','placeholder': 'confirm password'}))
    
    class Meta():
       model=User
       fields = ['email', 'username', 'password1', 'password2']
       class Media:
            css = {
                'all': ('css/style.css',)
            }

          

class AddImageForm(ModelForm):
    class Meta():
        model=Image
        fields=['image', 'image_name', 'image_caption']
        widgets = {
            'image': forms.FileInput(attrs={'class':'form-control  mb-3'}),
            'image_name': forms.TextInput(attrs={'class':'form-control mb-3'}),
            'image_caption': forms.Textarea(attrs={'class':'form-control mb-3'})
        }
        class Media:
            css = {
                'all': ('css/style.css',)
            }

class UpdateImageForm(ModelForm):
    class Meta():
        model=Image
        fields=['image_caption']
        widgets = {
            'image_caption': forms.Textarea(attrs={'class':'form-control mb-3'})
        }
        class Media:
            css = {
                'all': ('css/style.css',)
            }

class UpdateProfileForm(ModelForm):
    class Meta():
        model=Profile
        fields=['profile_photo', 'bio', 'name']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class':'form-control mb-3'}),
            'bio': forms.TextInput(attrs={'class':'form-control mb-3'}),
            'name': forms.TextInput(attrs={'class':'form-control mb-3'}),
        }
        class Media:
            css = {
                'all': ('css/style.css',)
            }