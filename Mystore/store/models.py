from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Banner(models.Model):
    banner_id=models.BigAutoField(primary_key=True,editable=False,db_column='banner_id')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    created_at=models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="banners/")
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = "Banners"
        
class Category(models.Model):
    category_id=models.BigAutoField(primary_key=True,editable=False,db_column='category_id')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    created_at=models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="categories/")

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Categories"    
        
class Product(models.Model):
    product_id=models.BigAutoField(primary_key=True,editable=False,db_column='product_id')
    title = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,db_column='category_id')
    image = models.ImageField(upload_to="products/")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Products"            

class ProductImage(models.Model):
    image_id=models.BigAutoField(primary_key=True,editable=False,db_column='image_id')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, null=True,db_column='product_id')
    name = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now=True)
    images = models.ImageField(upload_to="Productimages/")

    @property
    def image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.images.url)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Products_Images"
COLORS = (
    ("no colors", "no colors"),
    ("Red", "Red"),
    ("Green", "Green"),
    ("Yellow", "Yellow"),
    ("Pink", "Pink"),
    ("Brown", "Brown"),
    ("Black", "Black"),
    ("White", "White"),
)

class ProductColor(models.Model):
    color_id=models.BigAutoField(primary_key=True,editable=False,db_column='color_id')
    Product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE, null=True,db_column='product_id')
    name = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now=True)
    colors = models.CharField(choices=COLORS, max_length=20, default="no colors")

    def __str__(self):
        return self.colors
    
    class Meta:
        db_table = "Products_Colors"        

SIZES = (
    ("no sizes", "no sizes"),
    ("uk=4", "uk-4"),
    ("uk-5", "uk-5"),
    ("uk-6", "uk-6"),
    ("uk-7", "uk-7"),
    ("uk-8", "uk-8"),
    ("uk-9", "uk-9"),
    ("uk-10", "uk-10"),

)


class ProductSize(models.Model):
    size_id=models.BigAutoField(primary_key=True,editable=False,db_column='size_id')
    Product = models.ForeignKey(Product, related_name='sizes',on_delete=models.CASCADE, null=True,db_column='product_id')
    name = models.CharField(max_length=255)
    sizes = models.CharField(choices=SIZES, max_length=100, default='no sizes')
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sizes
    
    class Meta:
        db_table = "Products_Sizes"
        
class Cart(models.Model):
    cart_id=models.BigAutoField(primary_key=True,editable=False,db_column='cart_id')
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True,db_column='user_id')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    complit = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    is_in_order = models.BooleanField(default=False)

    def __str__(self):
        return "Cart: " + str(self.id)
    
    class Meta:
        db_table = "Cart"        

class CartProduct(models.Model):
    cartitem_id=models.BigAutoField(primary_key=True,editable=False,db_column='cartitem_id')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,db_column='cart_id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, default="no_color", on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, default="no_sizes", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.PositiveBigIntegerField(default=100)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Qualtity=={self.quantity}"
    
    class Meta:
        db_table = "Cart_Items"


class ShippingAddress(models.Model):
    shipping_id=models.BigAutoField(primary_key=True,editable=False,db_column='shipping_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,db_column='user_id')
    name = models.CharField(max_length=55)
    city = models.CharField(max_length=55)
    pincode = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    destinationtype = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Shipping_Address"


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),
)



class Order(models.Model):
    order_id=models.BigAutoField(primary_key=True,editable=False,db_column='order_id')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE,db_column='cart_id')
    ordered_by = models.CharField(max_length=200)
    address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=False)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)
    
    class Meta:
        db_table = "Product_Orders"                


class UploadFile(models.Model):
    file_id=models.BigAutoField(primary_key=True,editable=False,db_column='file_id')
    fileName = models.CharField(max_length=150, blank=False, null=False)
    fileDesc = models.CharField(max_length=150, blank=False, null=False)
    myfile = models.FileField(upload_to="uploads/")
    created_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Uploads"        