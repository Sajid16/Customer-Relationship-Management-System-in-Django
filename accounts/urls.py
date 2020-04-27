from django.urls import path
from accounts import views

urlpatterns = [
    # path('test/', include('test_app.urls')),
    path('', views.home, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOutUser, name='logout'),
    path('products/', views.products, name='products'),
    path('user_profile/', views.userProfile, name='user_profile'),
    path('create_order/<str:pk>/', views.createOrder, name='createOrder'),
    path('update_order/<str:pk>', views.updateOrder, name='updateOrder'),
    path('customer_update_order/<str:pk>/<str:customer_id>/', views.individualCustomerUpdateOrder, name='individualCustomerUpdateOrder'),
    path('delete_order/<str:pk>', views.deleteOrder, name='deleteOrder'),
    path('customer_delete_order/<str:pk>/<str:customer_id>/', views.individualCustomerDeleteOrder, name='individualCustomerDeleteOrder'),
    path('customer/<str:pk>/', views.customer, name='customer'),
]
