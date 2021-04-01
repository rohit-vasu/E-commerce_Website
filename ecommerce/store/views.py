from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import CreateUserForm
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import json
from .filter import ProductFilter
from .models import  *

# Create your views here.
def authUser(request):
	if request.user.is_authenticated:
		customer =request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems= order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0}
		cartItems = order['get_cart_items']
	return {'cartItems':cartItems,'items':items,'order':order}

def store(request):
	allitems =	authUser(request)
	cartItems = allitems['cartItems']
	hotproducts = Product.objects.filter(tags__name="Hot")
	tddproducts = Product.objects.filter(tags__name="Today's Deals")
	ltpproducts = Product.objects.filter(tags__name="Limited Time Offers")
	context = {'hotproducts':hotproducts,'ltpproducts':ltpproducts,'tddproducts':tddproducts,'cartItems':cartItems,'shipping':False}
	return render(request, 'store/store.html', context)

def cart(request):
	allitems =	authUser(request)
	items = allitems['items']
	order = allitems['order']
	cartItems = allitems['cartItems']
	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	allitems =	authUser(request)
	items = allitems['items']
	order = allitems['order']
	cartItems = allitems['cartItems']
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

@login_required(login_url = 'login')
def profile(request,pk):
	allitems =	authUser(request)
	cartItems = allitems['cartItems']
	customer = Customer.objects.get(id = pk)
	context = {'customer': customer,'cartItems':cartItems}
	return render(request, 'store/profile.html', context)

def productDetail(request,pk):
	form = CommentForm()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		form.instance.product = Product.objects.get(id = pk)
		if form.is_valid():
			form.save()
			return redirect(request.path_info)
		else:
			messages.info(request,'Error You entered blank Comment')
			return redirect('store')
	allitems =	authUser(request)
	cartItems = allitems['cartItems']
	#comments = Comment.objects.all()
	product = Product.objects.get(id = pk)
	context = {'product':product,'cartItems':cartItems,'form':form}
	return render(request, 'store/pdp.html', context)

def faq(request):
	context = {}
	return render(request, 'store/FAQ.html', context)

def about(request):
	context = {}
	return render(request, 'store/AboutUs.html', context)

def search(request):
	allitems =	authUser(request)
	cartItems = allitems['cartItems']
	products = Product.objects.all()
	myFilter = ProductFilter(request.GET,queryset=products)
	products = myFilter.qs
	context = {'myFilter':myFilter,'products':products,'cartItems':cartItems}
	return render(request, 'store/search.html', context)