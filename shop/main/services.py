from django.contrib.auth.models import User, auth
from django.shortcuts import redirect
from .models import Categories, Basket


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

def get_categories_query():
    return Categories.objects.all()

def get_user_products_in_basket(user_id):
    user = User.objects.get(id=user_id)

    products_in_basket = Basket.objects.filter(user = user)

    #find amount of all products in basket
    counter_each_products_in_basket = 0
    for product in products_in_basket:
        counter_each_products_in_basket += product.amount

    return counter_each_products_in_basket