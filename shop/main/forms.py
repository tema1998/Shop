from django import forms

from django.core.exceptions import ValidationError

from .services import check_username_exists, check_email_exists, signin_authenticate


class SignUpForm(forms.Form):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='E-mail', max_length=50)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль')
    password_repeated = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите пароль')

    def clean_username(self):
        username = self.cleaned_data['username']

        if check_username_exists(username):
            raise ValidationError('Логин уже занят')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if check_email_exists(email):
            raise ValidationError('E-mail адрес уже используется')

        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data['password']
        password_repeated = cleaned_data['password_repeated']

        if password != password_repeated:
            # raise ValidationError('Первый вариант вывода сообщений')
            self.add_error('password', 'Пароли не совпадают')
            self.add_error('password_repeated', 'Пароли не совпадают')

        return cleaned_data


class SignInForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     username = cleaned_data['username']
    #     password = cleaned_data['password']
    #
    #     user_authenticate = signin_authenticate(request, username, password)
    #
    #     if user_authenticate is None:
    #         self.add_error('username', 'Логин/пароль введены не верно')
    #
    #     return cleaned_data
