from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Category, Post

class ContactForm(forms.Form):
    name=forms.CharField(max_length=225,label='name',required=True)
    email=forms.EmailField(label='email',required=True)
    message=forms.CharField(label='message',max_length=255,required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='username',max_length=255,required=True)
    email = forms.EmailField(label='email',max_length=255,required=True)
    password = forms.CharField(label='password',max_length=255,required=True)
    password_confirm = forms.CharField(label='confirm password',max_length=255,required=True)

    class Meta:
        model = User
        fields=[
            'username','email','password'
        ]
    
    def clean(self):
        cleaned_data=super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password !=password_confirm:
            raise forms.ValidationError("Password dont Match")
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255,label='username',required=True)
    password = forms.CharField(label='password',max_length=255,required=True)

    def clean(self):
        cleaned_data=super().clean()
        username=cleaned_data.get('username')
        password=cleaned_data.get('password')
        if username and password :
            user = authenticate(username=username,password=password)
            if user is None :
                raise forms.ValidationError("Invalid  User Name and Password")


class ForgotPasswordForm(forms.Form):
    email =forms.EmailField(max_length=255,required=True,label='email')

    def clean(self):
        cleaned_data=super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('No User Found using This email')
        
class ResetPasswordForm(forms.Form):
   new_password= forms.CharField(label='New Password',max_length=255,required=True)
   confirm_password = forms.CharField(label='Confirm Password',max_length=255,required=True)

   def clean(self):
        cleaned_data=super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password !=confirm_password:
            raise forms.ValidationError("Password dont Match")
        


class PostForm(forms.ModelForm):
    title=forms.CharField(max_length=255,required=True,label='Title')
    content=forms.CharField(required=True,label='Content')
    category=forms.ModelChoiceField(label='Category',required=True,queryset=Category.objects.all())
    


    class Meta:
        model=Post
        fields=['title','content','category']


    def clean(self):
        cleaned_data= super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and len(title)<5:
            raise forms.ValidationError("Title must be Atleast 5 Character long")
        if content and len(content)<10:
            raise forms.ValidationError("Content must be Atleast 5 Character long")