from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from shopApp.models import *
from django.db.models import Q
from .forms import *
from cart.forms import CartAddProductForm
from .models import UserProfile
from .forms import UserProfileForm

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
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'home.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


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

    reviews = Review.objects.filter(product_id = product_id)
    
    cart_product_form = CartAddProductForm()
    return render(request,
                  'product_detail.html',
                  {'product': product,'reviews':reviews,'cart_product_form': cart_product_form})


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(product__id=product_id)
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
    #orders = profile.orders.all()

    
    context = {
        'form': form
    
        
    }

    return render(request, "profile.html", context)
