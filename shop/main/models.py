from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.CharField(max_length=100, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Товар')
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='Слаг')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')
    description = models.CharField(max_length=500, verbose_name='Описание')
    stock = models.PositiveIntegerField(verbose_name='Кол-во')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Со скидкой')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='basket')
    amount = models.PositiveIntegerField()
    first_added_at = models.DateTimeField(auto_now_add=True)
    last_added_at = models.DateTimeField(auto_now=True)