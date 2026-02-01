from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Comment, ProfileUser


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password = forms.CharField(label='Пароль пользователя', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    username = UsernameField(label='Придумайте логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')



class CommentForm(forms.ModelForm):
    text = forms.CharField(label='оставить комментарий', widget=forms.Textarea(attrs={
        'class': 'form-control bg-dark text-light mt-2',
        'style': 'height: 100px;'
    }))

    class Meta:
        model = Comment
        fields = ('text', )




class EditAccountForm(forms.ModelForm):
    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    username = UsernameField(label='Ваш логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    old_password = forms.CharField(required=False, label='Старый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password = forms.CharField(required=False, min_length=8, label='Новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(required=False, min_length=8, label='Повторить пароль',
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control'
                                   }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'old_password', 'new_password', 'confirm_password')



class EditProfileUserForm(forms.ModelForm):
    location = forms.CharField(required=False, max_length=50, label='От куда вы', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    about = forms.CharField(required=False, max_length=300, label='О себе', widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

    photo = forms.ImageField(required=False, label='Фото', widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = ProfileUser
        fields = ('location', 'photo', 'about')






















