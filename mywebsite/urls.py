"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from posts.views import (
    post_details_view,
    post_create_view,
    search_view,
)

from marketing.views import (
    dismiss_marketing_message,
    email_signup,
)

from cart.views import (
    cart_view,
    add_to_cart_view,
    remove_from_cart_view,
)

from store.views import (
    category_view,
    store_main_view,
    item_detail_view,
)
from orders.views import (
    checkout_view,
    orders_view,
    payment_page_view,
    checkout_final_view,
    payment_successful_view,
    payment_failed_view,
)
from accounts.views import (
    activation_view,
    add_user_address,
    logout_view,
    login_view,
    registration_view,
)
from mywebsite.views import (
    test_view,
    capital_word_view, 
    home_view,
    capital_word_result_view,
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('capital/', capital_word_view, name='capital-word'),
    path('posts/create/', post_create_view, name='post-create'),
    path('store/main/', store_main_view, name='store-main'),
    path('search/', search_view, name='search-results'),
    path('posts/<slug:pizda>/', post_details_view, name='post-details'),
    path('capital/result/', capital_word_result_view, name='capital-word-result'),
    path('store/items/<slug:anal>/', item_detail_view, name='item-detail'),
    path('store/cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('orders/', orders_view, name='orders'),
    path('ajax/dismiss-marketing-message', dismiss_marketing_message, name='dismiss-marketing-message'),
    path('ajax/email-signup', email_signup, name='ajax-email-signup'),
    path('store/cart/<int:id>/', remove_from_cart_view, name='remove-from-cart'),
    path('store/cart/<slug:hueta>/', add_to_cart_view, name='add-to-cart'),
    path('store/<slug:vagina>/', category_view, name='category'),
    path('test/', test_view, name='test'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/register/', registration_view, name='register'),
    path('accounts/activate/<str:activation_key>/', activation_view, name='activation'),
    path('accounts/address/add', add_user_address, name='add_user_address'),
    path('ajax/add-user-address/', add_user_address, name='ajax-add-user-address'),
    
    path('checkout/payment-successful', payment_successful_view, name='payment-successful'),
    path('checkout/payment-failed', payment_failed_view.as_view(), name='payment-failed'),

    path('checkout/pre-payment/', payment_page_view, name='payment-page'),
    path('checkout/final-payment/<id>/', checkout_final_view, name='checkout-final-page'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
















    # path('store/cart/', cart_view, name='cart'),
    # path('store/cart/<slug:slug>/', update_cart, name='update-cart'),
