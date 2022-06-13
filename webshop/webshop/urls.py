"""webshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from shopApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name = "welcome"),
    path("register", views.register, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("home/",views.home,name="home"),
    path("about", views.about, name="about"),
    path("profile/", views.profile, name = "profile"),
    path('(?P<category_slug>[-\w]+)/',views.home,name='home_by_category'),
    path("search/",views.search,name="search"),
    path('orders/', include('orders.urls', namespace='orders')),
    path('(?P<product_id>\d+)/(?P<slug>[-\w]+)/',views.product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('cart/', include('cart.urls', namespace='cart')),
    #paypal payment
    path('process/$', views.payment_process
        , name='process'),
    path('payment_done/$', views.payment_done
        , name='payment_done'),
    path('payment_cancelled/$', views.payment_cancelled
        , name='payment_cancelled'),
    path('paypal/', include("paypal.standard.ipn.urls")),

    #wishlist
    path('favourite/', views.favourite_list, name='favourite_list'),
    path('favourite/(?P<product_id>\d+)', views.favourite, name='favourite'),
    path('delete/<int:product_id>/', views.delete, name='delete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
