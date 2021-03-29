from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
import json

from .models import  *

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer =request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems,'shipping':False}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer =request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer =request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action : ',action,'productId : ',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item Was added', safe=False)

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + ', Your Account Creation was Successfull..')
            return redirect('login')
    context = {'form':form}
    return render(request, 'store/registerpage.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user) 
            return redirect('store')
        else:
            messages.info(request,'Username or Password is not Correct')
    context = {}
    return render(request, 'store/loginpage.html', context)

def OurTeam(request):
    context = {}
    return render(request, 'store/Our-Team.html', context)