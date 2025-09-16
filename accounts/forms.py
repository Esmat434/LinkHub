import uuid
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    ForgotPassword
)

User=get_user_model()

class RegisterForm(forms.ModelForm):
    confirm_password=forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                "placeholder":'Enter your confirm password'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username','email','avatar',"password"
        )
        widgets = {
            'username':forms.TextInput(
                attrs={
                    'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                    'placeholder':'Enter your username',
                    'required':True
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                    'placeholder':'Enter your email',
                    "required":True
                }
            ),
            "avatar":forms.FileInput(
                attrs={
                    'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300'
                }
            ),
            "password":forms.PasswordInput(
                attrs={
                    'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                    'placeholder':'Enter your password'
                }
            )
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password',None)
        confirm_password = cleaned_data.get('confirm_password',None)

        if not password or not confirm_password:
            raise forms.ValidationError("Please enter password and confrim password.")
        
        if len(password)<8:
            raise forms.ValidationError("Your password must be 8 or more characters.")
        
        if password != confirm_password:
            raise forms.ValidationError("Your password do not match with confrim password.")
        
        return cleaned_data
    
    def save(self, commit = True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                'placeholder':'Enter your username.'
            }
        )
    )
    password = forms.CharField(
        max_length=128, 
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                'placeholder':'Enter your password.'
            }
        )
    )

    def clean_username(self):
        username=self.cleaned_data.get('username')

        if not username:
            raise forms.ValidationError("Please enter your username.")

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username does not exists.")

        return username        

    def clean(self):
        cleaned_data = super().clean()
        password=cleaned_data.get('password')

        if not password:
            raise forms.ValidationError("Please enter your password.")
        
        if len(password)<8:
            raise forms.ValidationError("Your password must be 8 or more characters.")
        
        return cleaned_data
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields = (
            'username','email','avatar'
        )
        widgets = {
            'username':forms.TextInput(
                attrs={
                    'class':'mt-1 block w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-gray-800 dark:text-white',
                    'placeholder':"Enter your username"
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class':'mt-1 block w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-gray-800 dark:text-white',
                    'placeholder':'Enter your email'
                }
            ),
            'avatar':forms.FileInput(
                attrs={
                    'class':'mt-1 block w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-gray-800 dark:text-white'
                }
            )
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError("This username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError("This email already exists.")
        return email
    

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                'placeholder':'Enter your email'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        if not email:
            raise forms.ValidationError("Please enter your email.")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Your don't have an account.")
        
        return cleaned_data
    
    def save(self):
        user=User.objects.get(email=self.cleaned_data['email'])
        new_token=uuid.uuid4()
        token,_ = ForgotPassword.objects.update_or_create(
            user=user,
            defaults={
                'token':new_token,
                'created_at':timezone.now()
            }
        )

        return token

class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(
        max_length=128, 
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                'placeholder':'Enter your password.'
            }
        )
    )
    confirm_password = forms.CharField(
        max_length=128, 
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'w-full py-3 pl-10 pr-4 bg-gray-50 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 transition-all duration-300',
                'placeholder':'Enter your cofirm password.'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password',None)
        confirm_password = cleaned_data.get('confirm_password',None)

        if not password or not confirm_password:
            raise forms.ValidationError("You must enter your password and confirm password.")
        
        if len(password)<8:
            raise forms.ValidationError("Your password must be 8 or more characters.")
        
        if password != confirm_password:
            raise forms.ValidationError("Your password do not match with confirm password.")
        
        return cleaned_data
    
    def save(self,user):
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user