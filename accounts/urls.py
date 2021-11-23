from django.urls import path
from . import views
urlpatterns = [
    path('',views.home , name='home'),
    path('userpage',views.userpage,name='userpage'),
    path('accsettings',views.accSettings,name='accsettings'),
    path('products',views.products,name='products'), 
    path('customer/<int:pk>',views.customer,name='customer' ),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('deleteorder/<str:pk>',views.deleteOrder,name='deleteorder'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logoutPage,name='logout'),
    path('register',views.register,name='register'),

]
