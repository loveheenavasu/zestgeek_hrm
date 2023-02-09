from django import forms
from .models import *

class RegisterForm(forms.Form):

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    role = forms.CharField()
    personal_email = forms.EmailField()
    gender = forms.CharField()
    image = forms.ImageField()
    temporary_address = forms.CharField()
    permanent_address = forms.CharField()
    phone_number = forms.IntegerField()
    alternate_phone_number = forms.IntegerField()
    department = forms.CharField()
    joined_date = forms.DateField()
    password = forms.CharField()
    confirm_password = forms.CharField()



    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError({'password': "password doest not matched"})



    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email already exists.')
        return email

