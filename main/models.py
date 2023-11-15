import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Extend default django user and used for front-end accounts
class CustomUser(AbstractUser):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


    # Differentiates buyer and seller acounts
    account_types = (
        ('B', 'Buyer'),
        ('S', 'Seller'),
        ('A', 'Admin')
    )
    account = models.CharField(max_length=1, choices=account_types)

    # Add related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class Product(models.Model):
    product_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_count = models.IntegerField(default=0)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='username') # Retrieve from CustomUser account = 'Seller'
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=200)

    def __str__(self):
       return self.name


class Review(models.Model):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ] 
    review_id = models.AutoField(primary_key= True)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='name') # Retrieve from product
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='username') # Retrieve from reviewer (CustomUser Account='B')
    comment = models.TextField()
    
    #created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class CustomerFeedback(models.Model):
    feedback_id = models.CharField(primary_key=True, max_length=30)  # Define it as a CharField
    respondent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='username')
    rating = models.PositiveSmallIntegerField(
        verbose_name="How satisfied are you with your shopping experience?",
        choices=[(i, str(i)) for i in range(1, 11)],
    )
    easy_to_navigate = models.BooleanField(
        verbose_name="Did you find the website easy to navigate?",
    )
    additional_categories = models.TextField(
        verbose_name="What products or categories would you like to see more of on our website?",
        blank=True,
    )
    information_found = models.BooleanField(
        verbose_name="Were you able to find the information you were looking for?",
    )
    recommendation_relevance = models.BooleanField(
        verbose_name="Do you find the recommended products relevant to your interest?"
    )
    recommendation_accuracy_rating= models.PositiveSmallIntegerField(
        verbose_name="How would you rate our product recommendation accuracy?", 
        choices=[(i, str(i)) for i in range(1, 11)],
    )
    comments = models.TextField(
        verbose_name="Any additional comments or suggestions for improvement?",
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.feedback_id:
            current_time = timezone.now()
            # Create a unique identifier using the current timestamp
            unique_id = 'C' + current_time.strftime("%Y%m%d%H%M%S%f")  # Prefix with 'C'
            self.feedback_id = unique_id
        super().save(*args, **kwargs)


class SellerFeedback(models.Model):
    feedback_id = models.CharField(primary_key=True, max_length=30)  # Define it as a CharField
    respondent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='username')
    rating = models.PositiveSmallIntegerField(
        verbose_name="How satisfied are you with your experience as a seller on our platform?",
        choices=[(i, str(i)) for i in range(1, 11)],
    )
    easy_to_sell = models.BooleanField(
        verbose_name="Was it easy to list your products on our platform?",
    )
    fee_structure = models.BooleanField(
        verbose_name="Were you satisfied with the payment process and fee structure?",
    )
    customer_support = models.PositiveSmallIntegerField(
        verbose_name="How would you rate the support provided to sellers by our customer support team?",
        choices=[(i, str(i)) for i in range(1, 11)],
    )
    comments = models.TextField(
        verbose_name="Any additional comments or suggestions for improvement?",
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.feedback_id:
            current_time = timezone.now()
            # Create a unique identifier using the current timestamp
            unique_id = 'S' + current_time.strftime("%Y%m%d%H%M%S%f")  # Prefix with 'S'
            self.feedback_id = unique_id
        super().save(*args, **kwargs)



class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total
    
    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.product.name
    
    @property
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price


class Order(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Yet to be completed', 'Yet to be completed'),
        ('Cancelled', 'Cancelled'),
    ]
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    buyer = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    order_created_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Yet to be completed')
    delivery_address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.order_id)
    
    @property
    def total_price(self):
        cartitems = self.orderitems.all()
        total = sum([item.price for item in cartitems])
        return total
    
    @property
    def num_of_items(self):
        cartitems = self.orderitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete= models.CASCADE, related_name="orderitems")
    quantity = models.IntegerField(default=0)
    
    STATUS_CHOICES = [
        ('To Ship', 'To Ship'),
        ('To Receive', 'To Receive'),
        ('Delivered', 'Delivered'),
    ]

    order_status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='To Ship')


    def __str__(self):
        return self.product.name
    
    @property
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price


class Payment(models.Model):
    order_id = models.ForeignKey(Order, on_delete= models.CASCADE, editable=False)
    payment_time = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)
    