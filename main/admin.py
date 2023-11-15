from typing import Any
from django import forms
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Cart, CartItem, CustomerFeedback, Order, OrderItem, Payment, SellerFeedback, Review, Product, CustomUser#, Reviewer 

def get_all_fields(model):
    """
    Get all fields (attributes) of the model.
    """
    return [field.name for field in model._meta.get_fields()]

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    #list_display = ('rating', 'user_id', 'product_id', 'comment')
    list_display = ('review_id', 'product_name', 'rating', 'username', 'comment')
    search_fields = ('product_name__name', 'rating', 'username__username', 'comment')
    list_filter = ('rating',)
    readonly_fields = list_display

    def has_add_permission(self, request):
        return False  # Disallow adding new feedback through the admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'sold_count', 'seller', 'description', 'image')
    search_fields = ('name', 'price', 'sold_count')  # Add fields you want to search by

class EmailFilter(admin.SimpleListFilter):
    title  = 'Email Filter'
    parameter_name = 'user_email'

    def lookups(self, request, model_admin):
        return (
            ('has_email', 'has email'),
            ('no_email', 'no email')
        )
    
    def queryset(self, request, queryset) :
        if not self.value():
            return queryset
        if self.value().lower() == 'has_email':
            return queryset.exclude(email='')
        if self.value().lower() == 'no_email':
            return queryset.filter(email='')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):


    

    fieldsets = (
        ('User Account Credentials', {
            'fields': ('username', 'password',),
            'description': 'Fields needed for login',
        }),
        ('User Info', {
            'fields': ('first_name', 'last_name', 'gender', 'email', 'phone_number','address'),
            'description': 'Personal info of users like name, gender, etc.',
        }),
        ('User Account Info', {
            'fields': ('account','is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login'),
            'description': 'Default user account info fields',
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'account','phone_number','address', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Add fields you want to search by
    list_filter = ('is_active', 'account', 'is_staff', 'gender', 'date_joined', EmailFilter)

    def has_add_permission(self, request):
        return False  # Disallow adding new user through admin

# @admin.register(Reviewer)
# class ReviewerAdmin(admin.ModelAdmin):
#     list_display = ('reviewer_id', 'username')


@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    #form = FeedbackAdminForm
    list_display = get_all_fields(CustomerFeedback)
    search_fields = ('respondent__username',)  # Add fields you want to search by
    readonly_fields = list_display
    list_filter = ('rating', 'recommendation_relevance', 'recommendation_accuracy_rating', 'timestamp')

    def has_add_permission(self, request):
        return False  # Disallow adding new feedback through the admin
    

@admin.register(SellerFeedback)
class SellerFeedbackAdmin(admin.ModelAdmin):
    #form = FeedbackAdminForm
    list_display = get_all_fields(SellerFeedback)
    search_fields = ('respondent__username',)  # Add fields you want to search by
    readonly_fields = list_display
    list_filter = ('rating', 'easy_to_sell', 'timestamp')

    def has_add_permission(self, request):
        return False  # Disallow adding new feedback through the admin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'buyer', 'order_created_time', 'order_status')
    search_fields = ('buyer__username', 'order_id')  # Add fields you want to search by
    readonly_fields = list_display
    list_filter = ('order_created_time', 'order_status')

    def has_add_permission(self, request):
        return False  # Disallow adding new feedback through the admin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_time', 'completed')
    search_fields = ('order_id',)  # Add fields you want to search by
    readonly_fields = list_display
    list_filter = ('payment_time', 'completed')

    def has_add_permission(self, request):
        return False  # Disallow adding new feedback through the admin


