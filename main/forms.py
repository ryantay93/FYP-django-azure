from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Review, CustomUser, CustomerFeedback, SellerFeedback
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from .models import Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    #name = forms.CharField(max_length = 100)
    gender_choices = (
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = forms.ChoiceField(
        choices = gender_choices,
        initial ='',  # Initially, no selection (placeholder)
        widget = forms.Select(attrs={'class': 'custom-select'}),
    )
    
    account_types = (
        ('', 'Select Account'),
        ('B', 'Buyer'),
        ('S', 'Seller')
    )
    account = forms.ChoiceField(
        choices = account_types,
        initial = '',
        widget = forms.Select(attrs={'class': 'custom-select'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'account', 'password1', 'password2', 'phone_number', 'address']

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = '<p class="form-text custom-help-text">' + self.fields['username'].help_text + '</p>'
        self.fields['password1'].help_text = '<p class="form-text custom-help-text">' + self.fields['password1'].help_text + '</p>'
        self.fields['password2'].help_text = '<p class="form-text custom-help-text">' + self.fields['password2'].help_text + '</p>'



class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email','phone_number', 'address']
        
    
    
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'sold_count', 'description', 'image']


class CustomerFeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = [
            'rating',
            'easy_to_navigate',
            'additional_categories',
            'information_found',
            'recommendation_relevance',
            'recommendation_accuracy_rating',
            'comments',
        ]


class SellerFeedbackForm(forms.ModelForm):
    class Meta:
        model = SellerFeedback
        fields = [
            'rating',
            'easy_to_sell',
            'fee_structure',
            'customer_support',
            'comments',
        ]


class PaymentForm(forms.Form):
    delivery_address = forms.CharField(max_length=200)






class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
