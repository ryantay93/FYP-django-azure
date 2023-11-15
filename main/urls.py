from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home', views.home, name = 'home'),
    path('sign-up', views.sign_up, name = 'sign_up'),
    path('add-product', views.add_product, name = 'add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('import/', views.import_from_excel, name='import_from_excel'),
    path('search/', views.search_products, name='search_products'),
    path('customer_feedback/', views.customer_feedback_view, name='customer_feedback_form'),
    path('seller_feedback/', views.seller_feedback_view, name='seller_feedback_form'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('view_account/', views.view_account, name='view_account'),
    path('change_password',views.change_password,name='change_password'),
    path('password_change_done',views.PasswordChangeDoneView.as_view(), name= 'password_change_done'),  
    path('delete_account',views.delete_account, name = 'delete_account'),  
    path('seller/my_products', views.SellerProductListView.as_view(), name='seller_products'),
    path('seller/my_products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('seller/my_products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('seller/<str:username>/store/', views.seller_store, name='seller_store'),

   ####
   
    path('admin_force_gen/', views.admin_force_gen, name='admin_force_gen'),
    path('buyer_recommendations/', views.buyer_recommendations, name='seller_store'),
    path('seller_predict_buyer/', views.seller_predict_buyer, name='seller_predict_buyer'),

   ####

    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('checkout', views.checkout, name='checkout'),

    path('review_success/<int:product_id>', views.review_success, name='review_success'),
    path('view_orders', views.buyer_view_orders, name='buyer_view_orders'),
    path('s_view_orders', views.seller_view_orders, name='seller_view_orders'),
    path('seller_create_report', views.seller_create_report, name='seller_create_report'),
    path('seller_download_report', views.seller_download_report, name='seller_download_report'),

    path('order_detail/<uuid:order_id>/', views.buyer_view_order_detail, name='order_detail'),
    #path('order_detail/<uuid:order_id>/', views.seller_view_order_detail, name='s_order_detail'),
    path('update_shipping_status/<str:order_id>/', views.update_shipping_status, name='update_shipping_status'),
    path('mark_received/<str:order_id>/', views.mark_received, name='mark_received'),
    path('save_review', views.save_review, name='save_review'),

]


#admin.site.index_title = 'E-commerce Website'
admin.site.site_header = 'Blue Moon'
admin.site.site_title = 'Admin Dashboard'
    





