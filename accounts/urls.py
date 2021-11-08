from django.urls import path
from . import views
urlpatterns = [
    path('',views.home , name='home'),
    path('products',views.products,name='products'), 
    path('customer/<int:pk>',views.customer,name='customer' ),
    path('createorder/<str:pk>',views.createOrder,name='createorder'),
    path('updateorder/<str:pk>',views.updateOrder,name='updateorder'),
    path('deleteorder/<str:pk>',views.deleteOrder,name='deleteorder'),

]
