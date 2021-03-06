from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    mobile = models.IntegerField(default=0,null=True,blank=True)
    dp = models.ImageField(null=True,blank=True)
    Country = models.CharField(max_length=200,default="N/A",null=True,blank=False)

    def __str__(self):
        return self.name

    @property
    def dpURL(self):
        try:
            url = self.dp.url
        except :
            url = 'images/avatar.png'
        return url

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    featured = models.ImageField(null=True,blank=True)
    description = models.TextField(default="No description available",null=True,blank=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.featured.url
        except :
            url = 'images/imagenotfound.png'
        return url
    
class Image(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	image = models.ImageField()

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		print('URL:', url)
		return url

class Comment(models.Model):
    RATING =(('Excellent','Excellent'),
    ('Very Good','Very Good'),
    ('Good','Good'),
    ('Average','Average'),
    ('Poor','Poor'))
    product = models.ForeignKey(Product,related_name="comments" ,on_delete=models.CASCADE)
    name = models.CharField(default="Anomynous",max_length=200)
    body = models.TextField(default="No description available",null=True,blank=False)
    date_commented = models.DateTimeField(auto_now_add=True)
    status = models.TextField(max_length=200,choices=RATING,blank=False)

    def __str__(self):
        return '%s - %s' % (self.product.name,self.name)

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
               shipping = True 
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Shipping(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    telephone = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.address



