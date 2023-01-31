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
from .models import Categories, Products
from .services import create_user_by_signup, user_signin_after_signup, signin_authenticate, signin_login_finish, is_user_signin



class Index(View):

    def get(self, request):
        products = Products.objects.all().order_by('-updated_at')

        paginated_products = Paginator(products, 3)
        page_number = request.GET.get('page')
        current_page_products = paginated_products.get_page(page_number)

        return render(request, 'main/index.html', {'products':current_page_products})

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