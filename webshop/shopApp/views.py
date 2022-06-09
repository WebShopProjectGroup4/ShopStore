from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render,get_object_or_404
from shopApp.models import *
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
                return redirect("registeration")
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect("registeration")
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
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'home.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, product_id,slug):
    product = get_object_or_404(Product,
                                id=product_id,
                                available=True)
    #cart_product_form = CartAddProductForm()
    return render(request,
                  'product_detail.html',
                  {'product': product,})