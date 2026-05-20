import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label='ФИО')
    phone = forms.CharField(max_length=20, label='Телефон')
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]{6,}$', username):
            raise forms.ValidationError('Логин должен содержать латиницу и цифры, минимум 6 символов')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[а-яА-ЯёЁ\s]+$', full_name):
            raise forms.ValidationError('ФИО должно содержать только буквы кириллицы и пробелы')
        return full_name
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise forms.ValidationError('Телефон должен быть в формате 8(XXX)XXX-XX-XX')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email