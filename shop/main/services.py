from django.contrib.auth.models import User, auth
from django.shortcuts import redirect
from .models import Products, Categories, Basket


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

def get_product_by_prod_id(id):
    return Products.objects.get(id=id)

def check_is_product_in_basket(user, product):
    return Basket.objects.filter(user=user, product=product).exists()

def add_new_product_to_basket(user, product, amount):
    new_product_in_basket = Basket.objects.create(user=user, product=product, amount=amount)
    new_product_in_basket.save()

def add_amount_of_product_to_basket(user, product, amount=1):
    exists_proudct_in_basket = Basket.objects.get(user=user, product=product)
    exists_proudct_in_basket.amount += amount
    exists_proudct_in_basket.save()
    if exists_proudct_in_basket.amount == 0:
        exists_proudct_in_basket.delete()

def delete_product_from_basket(user, product):
    exists_proudct_in_basket = Basket.objects.get(user=user, product=product)
    exists_proudct_in_basket.delete()