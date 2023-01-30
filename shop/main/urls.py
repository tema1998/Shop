from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('signin', views.Signin.as_view(), name='signin'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('/<str:slug>', views.ProductDetail.as_view(), name='product-detail'),
    path('category/<str:slug>', views.Category.as_view(), name='category'),
]