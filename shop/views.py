from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, Profile
from .forms import LoginForm, UserRegistrationForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout


def index(request):
    return HttpResponse("<h1>Hello world!</h1>")


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/list.html', {'category': category, 'categories': categories, 'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, available=True)
    profile = get_object_or_404(Profile, id=product.owners.id)
    productnew = Product.objects.filter(available=True, owners_id=product.owners.id)
    return render(request, 'shop/detail.html', {'products': product, 'profile': profile, 'productnew': productnew})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return redirect('product_list')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('product_list')
                else:
                    return HttpResponse('Account disabled')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('product_list')


@login_required(login_url='/login/')
def create_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            my_owner = Profile.objects.get(user=request.user)
            product.owners = my_owner
            product.save()
            return redirect(product)
    else:
        form = ProductForm
    return render(request, 'shop/add_product.html', {'form': form, 'categories': categories})

