from django.urls import path

from .views import *

urlpatterns = [
    path('', GuitarsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addproduct/', AddPage.as_view(), name='add_product'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<int:cat_id>/', show_category, name='category'),
    path('userposts/<slug:user_name>/', show_user_posts, name='user_posts'),

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart_detail/', cart_detail, name='cart_detail'),
    path('cart/successfully_purchased/', successfully_purchased, name='purchase'),
]
