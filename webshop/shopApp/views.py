from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from shopApp.models import *
from orders.models import *
from django.db.models import Q
from .forms import *
from cart.forms import CartAddProductForm
from .models import UserProfile
from .forms import UserProfileForm
from orders.models import *

from django.core.paginator import Paginator

#paypal
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def welcome(request):
    return render(request,"welcome.html")

def logout_user(request):
    auth.logout(request)
    return redirect('welcome')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('welcome')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')



    else:
        return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('login')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect("registeration")
            

    else:
        return render(request, 'registeration.html')




# Create your views here.

def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(Product.objects.all(), 5) 
    #page_number = request.GET.get('home')
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'home.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'page_obj':page_obj})


def search(request):
   
    if request.method == "POST":
        search = request.POST['search']
        
        products = Product.objects.filter(Q(name__icontains=search)|Q(description__icontains = search))
        
        return render(request, "search.html", {'search':search, 'products':products})
    else:
        return render(request, "search.html")


def product_detail(request, product_id,slug):
    product = get_object_or_404(Product,
                                id=product_id,
                                available=True)
    categories = Category.objects.all()

    reviews = Review.objects.filter(product_id = product_id)
    
    cart_product_form = CartAddProductForm()
    return render(request,
                  'product_detail.html',
                  {'product': product,'reviews':reviews,'cart_product_form': cart_product_form,'categories': categories,})


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(user=request.user,product_id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.title = form.cleaned_data['title']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.product_id = product_id
                user = request.user.id
                data.user_id = user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def about(request):
    return render(request,"about.html")

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        else:
            print("not valid")
    else:
        form = UserProfileForm(instance=profile)
   
    orders = OrderItem.objects.all()
    print(123)
    
    

    
    context = {
        'form': form,
        'orders':orders,
        
    }

    return render(request, "profile.html", context)


#payment
def payment_process(request):
    order_id = request.session.get('order_id')
    print(order_id)
    
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()#Returns the originating host 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,#business this is your Paypal account email. Payments will be sent to this account, 
        'amount': '%.2f' % order.get_total_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'SEK',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,
                  'payment/process.html',
                  {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment/cancelled.html')


#wishlist
def favourite(request,product_id):
    print(product_id)
    product=get_object_or_404(Product,id=product_id)
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
    else:
        product.favourite.add(request.user)
    return HttpResponseRedirect(product.get_absolute_url())

def favourite_list(request):
    user=request.user
    favourite_products = user.favourite.all()
    context={'favourite_products':favourite_products,}
    return render(request,'favourite.html',context)

def delete(request,product_id):
    products = Product.objects.get(id=product_id)
    print(product_id)
    if request.method == "POST":
        products.delete()
    
    user=request.user
    favourite_products = user.favourite.all()
    context={'favourite_products':favourite_products,}
    return render(request,'favourite.html',context)
    #return render(request,"home.html",{'products':products})

