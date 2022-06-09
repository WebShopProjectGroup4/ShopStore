from operator import mod
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        return reverse('home_by_category',
                       args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='images',blank = True)
    description = models.TextField(max_length = 1000,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=0)
    available = models.BooleanField(default=True)

    SIZES = (
        ('XS', 'XSmall'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    size = models.CharField(max_length=2, choices=SIZES)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.id,self.slug])


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=1000,blank=True)
    title = models.CharField(max_length=100,blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return " Review: " + str(self.title) 
