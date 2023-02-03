from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404


from .forms import SignUpForm, SignInForm
from .models import Categories, Products, Basket
from .services import create_user_by_signup, user_signin_after_signup, signin_authenticate, signin_login_finish, \
    is_user_signin, add_new_product_to_basket,add_amount_of_product_to_basket, check_is_product_in_basket, \
    get_product_by_prod_id, delete_product_from_basket



class Index(View):

    def get(self, request):
        products = Products.objects.all().order_by('-updated_at')

        paginated_products = Paginator(products, 3)
        page_number = request.GET.get('page')
        current_page_products = paginated_products.get_page(page_number)

        return render(request, 'main/index.html', {'products':current_page_products})

    def post(self, request):
        user = request.user
        chosen_product_id = request.POST['product_id']
        amount = 1

        product = get_product_by_prod_id(id=chosen_product_id)

        if check_is_product_in_basket(user=user, product=product):
            add_amount_of_product_to_basket(user=user, product=product)
            return redirect('index')
        else:
            add_new_product_to_basket(user=user, product=product, amount=amount)
            return redirect('index')


class ProductDetail(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, slug):
        current_product = Products.objects.filter(slug=slug).first
        if current_product:
            pass
        else:
            raise Http404
        return render(request, 'main/product_detail.html', {'current_product': current_product})

class Signup(View):

    def post(self, request):

        form = SignUpForm(request.POST if request.POST else None)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            create_user_by_signup(username = username, email = email, password = password)
            user_signin_after_signup(request=request, username=username, password=password)

            return redirect('index')

        return render(request, 'main/signup.html', {'form':form})


    def get(self, request):
        form = SignUpForm()
        return render(request, 'main/signup.html', {'form':form})


class Signin(View):

    def post(self, request):

        form = SignInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']


            user_authenticated = signin_authenticate(request=request, username=username, password=password)
            signin_login_finish(request=request, user_authenticated = user_authenticated)


            return redirect('index')

        return render(request, 'main/signin.html', {'form': form})

    def get(self, request):
        form = SignInForm()
        return render(request, 'main/signin.html', {'form': form})

class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('signin')


class Category(View):

    def get(self, request, slug):
        category = Categories.objects.filter(slug=slug).first()
        products = Products.objects.filter(category=category).order_by('stock' ,'-updated_at')

        paginated_products = Paginator(products, 3)
        page_number = request.GET.get('page')
        current_page_products = paginated_products.get_page(page_number)

        return render(request, 'main/category.html', {'products':current_page_products, 'category':category})


class BasketProducts(View):

    def get(self, request):
        user = request.user
        products_in_basket = Basket.objects.filter(user=user).order_by('-last_added_at')

        paginated_products = Paginator(products_in_basket, 3)
        page_number = request.GET.get('page')
        current_page_products = paginated_products.get_page(page_number)

        return render(request, 'main/basket.html', {'basket_model_products':current_page_products})

    def post(self, request):
        user = request.user
        chosen_product_id = request.POST['product_id']
        # amount = 1
        #
        current_product = Products.objects.get(id=chosen_product_id)

        if 'increase_amount' in request.POST:
            add_amount_of_product_to_basket(user, product=current_product, amount=1)
            return redirect('basket')

        if 'decrease_amount' in request.POST:
            add_amount_of_product_to_basket(user, product=current_product, amount=-1)
            return redirect('basket')

        if 'delete_product' in request.POST:
            delete_product_from_basket(user, product=current_product)
            return redirect('basket')