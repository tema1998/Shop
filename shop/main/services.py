from django.contrib.auth.models import User, auth
from django.shortcuts import redirect


def check_username_exists(username):
    return User.objects.filter(username=username).exists()


def check_email_exists(email):
    return User.objects.filter(email=email).exists()

def create_user_by_signup(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

def user_signin_after_signup(request, username, password):
    user_login = auth.authenticate(username=username, password=password)
    auth.login(request, user_login)

def signin_authenticate(request, username, password):
    user_authenticate = auth.authenticate(username=username, password=password)
    return user_authenticate

def signin_login_finish(request, user_authenticated):
    auth.login(request, user_authenticated)

def is_user_signin(username):

        current_user_object = User.objects.filter(username=username).first()
        if current_user_object is not None:
            return True
        else:
            return False